#!/usr/bin/env python3
"""
minipdf.py
==========
A tiny, zero-dependency PDF writer (pure standard library) sufficient to render
the tracker's paper as a paginated, readable PDF in any cron environment where
pandoc / weasyprint / fpdf2 are unavailable.

Supports: multi-page flow, word-wrapped paragraphs, three heading sizes, bold-ish
headings (via Helvetica-Bold), and simple bullet lines. Uses the built-in
Helvetica fonts (no embedding). Not a full markdown renderer -- it consumes a
lightweight block list produced by md_to_blocks().
"""
from __future__ import annotations

import re
from pathlib import Path

# Helvetica average glyph width approximation (in 1/1000 em) for wrapping.
_AVG_W = 0.50  # conservative; keeps lines from overflowing the right margin.


def _esc(t: str) -> str:
    return t.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def _wrap(text: str, size: float, max_w: float) -> list[str]:
    max_chars = max(8, int(max_w / (size * _AVG_W)))
    out, line = [], ""
    for word in text.split():
        cand = word if not line else f"{line} {word}"
        if len(cand) <= max_chars:
            line = cand
        else:
            if line:
                out.append(line)
            # hard-break very long tokens (e.g. URLs)
            while len(word) > max_chars:
                out.append(word[:max_chars])
                word = word[max_chars:]
            line = word
    if line:
        out.append(line)
    return out or [""]


class Block:
    __slots__ = ("kind", "text")

    def __init__(self, kind: str, text: str):
        self.kind = kind  # h1 h2 h3 p bullet quote rule
        self.text = text


def md_to_blocks(md: str) -> list[Block]:
    """Very small markdown -> block converter (headings, paragraphs, bullets,
    blockquotes, tables-as-text, hr). YAML front matter is stripped."""
    md = re.sub(r"^---\n.*?\n---\n", "", md, count=1, flags=re.DOTALL)
    blocks: list[Block] = []
    for raw in md.split("\n"):
        s = raw.rstrip()
        if not s.strip():
            continue
        if s.startswith("### "):
            blocks.append(Block("h3", s[4:]))
        elif s.startswith("## "):
            blocks.append(Block("h2", s[3:]))
        elif s.startswith("# "):
            blocks.append(Block("h1", s[2:]))
        elif s.startswith(("- ", "* ")):
            blocks.append(Block("bullet", s[2:]))
        elif s.startswith("> "):
            blocks.append(Block("quote", s[2:]))
        elif set(s.strip()) <= {"-", "|", ":", " "} and "|" in s:
            continue  # table separator row -> skip
        else:
            # strip common markdown emphasis/link syntax for clean text
            s = re.sub(r"\*\*(.*?)\*\*", r"\1", s)
            s = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1 (\2)", s)
            blocks.append(Block("p", s))
    return blocks


def render(blocks: list[Block], out_path: Path, title: str = "") -> None:
    PW, PH = 612, 792          # US Letter points
    ML, MR, MT, MB = 60, 60, 72, 60
    max_w = PW - ML - MR
    leading = 1.32

    pages: list[list[str]] = []
    cur: list[str] = []
    y = PH - MT

    def newpage():
        nonlocal cur, y
        if cur:
            pages.append(cur)
        cur, y = [], PH - MT

    def emit(text: str, size: float, font: str, gap_before: float, gap_after: float, indent: float = 0):
        nonlocal y
        y -= gap_before
        for ln in _wrap(text, size, max_w - indent):
            if y < MB:
                newpage()
            cur.append(
                f"BT /{font} {size:g} Tf 1 0 0 1 {ML+indent:g} {y:g} Tm ({_esc(ln)}) Tj ET"
            )
            y -= size * leading
        y -= gap_after

    style = {
        "h1": (17, "F2", 14, 6),
        "h2": (14, "F2", 14, 5),
        "h3": (12, "F2", 10, 3),
        "p":  (10.5, "F1", 0, 6),
        "bullet": (10.5, "F1", 0, 3),
        "quote": (10.5, "F3", 2, 6),
    }
    for b in blocks:
        if b.kind == "bullet":
            size, font, gb, ga = style["bullet"]
            emit("• " + b.text, size, font, gb, ga, indent=14)
        elif b.kind in style:
            size, font, gb, ga = style[b.kind]
            indent = 18 if b.kind == "quote" else 0
            emit(b.text, size, font, gb, ga, indent=indent)
    newpage()

    # ---- assemble PDF objects ----
    fonts = {"F1": "Helvetica", "F2": "Helvetica-Bold", "F3": "Helvetica-Oblique"}
    objs: list[bytes] = []

    def add(b: bytes) -> int:
        objs.append(b)
        return len(objs)

    font_ids = {}
    for fid, base in fonts.items():
        n = add(f"<< /Type /Font /Subtype /Type1 /BaseFont /{base} >>".encode())
        font_ids[fid] = n

    page_obj_ids, content_ids = [], []
    for page in pages:
        stream = "\n".join(page).encode("latin-1", "replace")
        cid = add(b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream))
        content_ids.append(cid)

    pages_id = len(objs) + len(pages) + 1  # placeholder; fix below
    # we need Pages object id known to kids; compute after creating page objs
    # create page objects referencing a Pages id we reserve now:
    reserved_pages_id = len(objs) + len(pages) + 1
    fontres = " ".join(f"/{fid} {font_ids[fid]} 0 R" for fid in fonts)
    for i, cid in enumerate(content_ids):
        pid = add(
            (f"<< /Type /Page /Parent {reserved_pages_id} 0 R "
             f"/MediaBox [0 0 {PW} {PH}] /Resources << /Font << {fontres} >> >> "
             f"/Contents {cid} 0 R >>").encode()
        )
        page_obj_ids.append(pid)
    kids = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
    pages_id = add(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_ids)} >>".encode())
    assert pages_id == reserved_pages_id, (pages_id, reserved_pages_id)
    catalog_id = add(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode())

    # ---- serialize with xref ----
    buf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for i, body in enumerate(objs, start=1):
        offsets.append(len(buf))
        buf += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref_pos = len(buf)
    n = len(objs) + 1
    buf += f"xref\n0 {n}\n".encode()
    buf += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        buf += f"{off:010d} 00000 n \n".encode()
    buf += (f"trailer\n<< /Size {n} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF").encode()
    out_path.write_bytes(buf)


def md_file_to_pdf(md_path: Path, pdf_path: Path) -> None:
    render(md_to_blocks(md_path.read_text()), pdf_path)


if __name__ == "__main__":
    import sys
    md_file_to_pdf(Path(sys.argv[1]), Path(sys.argv[2]))
    print(f"wrote {sys.argv[2]}")
