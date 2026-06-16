#!/usr/bin/env python3
"""Export the generated paper to PDF, DOCX, and standalone HTML via pandoc.

The Markdown paper (``Doc/index.md``) is the single source; this produces the
downloadable document artifacts. DOCX and standalone HTML never need a LaTeX
engine; PDF is attempted with whatever engine is available (tectonic / xelatex /
pdflatex / wkhtmltopdf) and skipped with a clear message if none is installed,
so a local build without TeX still succeeds.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import dataio  # noqa: E402

SRC = dataio.DOC_DIR / "index.md"
OUT_DIR = dataio.DOC_DIR / "exports"
BASENAME = "Dario-Amodei-Prediction-Tracker"

# The default LaTeX fonts lack emoji and some symbols; swap them for ASCII so
# the PDF renders cleanly. (HTML/DOCX keep the originals.)
_PDF_SUBS = {
    "✅": "[achieved]", "🟡": "[partial]", "🔵": "[in window]",
    "🟣": "[pending]", "🔴": "[missed]", "⚪": "[unverifiable]",
    "→": "->", "★": "*", "○": "o", "·": "-",
}


def _sanitize_for_pdf(text: str) -> str:
    for k, v in _PDF_SUBS.items():
        text = text.replace(k, v)
    return text


def _have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _pdf_engine() -> str | None:
    for eng in ("tectonic", "xelatex", "pdflatex", "wkhtmltopdf"):
        if _have(eng):
            return eng
    return None


def _run(args: list[str]) -> bool:
    print("  $ " + " ".join(args))
    try:
        subprocess.run(args, check=True, cwd=dataio.DOC_DIR)
        return True
    except subprocess.CalledProcessError as exc:
        print(f"  ! pandoc failed ({exc.returncode})", file=sys.stderr)
        return False


def main() -> int:
    if not _have("pandoc"):
        print("pandoc not installed — skipping PDF/DOCX/HTML export.\n"
              "  Install pandoc (and a LaTeX engine for PDF) to enable this step.")
        return 0
    if not SRC.exists():
        print(f"{SRC} missing — run Scripts/build_paper.py first.", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    common = ["--standalone", "--resource-path=.", f"--metadata=date:{dataio._dt.date.today().isoformat()}"]

    ok = True
    # DOCX (no LaTeX needed)
    ok &= _run(["pandoc", "index.md", *common, "--toc",
                "-o", f"exports/{BASENAME}.docx"])
    # Standalone HTML (no LaTeX needed)
    ok &= _run(["pandoc", "index.md", *common, "--toc", "--mathjax", "--embed-resources",
                "-o", f"exports/{BASENAME}.html"])
    # PDF (needs an engine). Render from an ASCII-sanitized temp copy.
    engine = _pdf_engine()
    if engine:
        pdf_src = dataio.DOC_DIR / "_pdf_src.md"
        pdf_src.write_text(_sanitize_for_pdf(SRC.read_text(encoding="utf-8")), encoding="utf-8")
        try:
            pdf_args = ["pandoc", "_pdf_src.md", *common, "--toc",
                        "-V", "geometry:margin=1in", "-V", "linkcolor:blue",
                        f"--pdf-engine={engine}", "-o", f"exports/{BASENAME}.pdf"]
            ok &= _run(pdf_args)
        finally:
            pdf_src.unlink(missing_ok=True)
    else:
        print("  (no LaTeX/PDF engine found — PDF skipped; DOCX + HTML produced)")

    print(f"Exports written to {OUT_DIR.relative_to(dataio.REPO_ROOT)}/")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
