#!/usr/bin/env bash
# Regenerate every artifact from the dataset: validate -> mathematics ->
# paper -> document exports -> static site. pandoc/mkdocs steps are skipped
# gracefully if those tools are not installed locally (CI installs them).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "==> [1/5] Validate dataset"
python Scripts/validate.py

echo "==> [2/5] Compute mathematics (metrics + figures)"
python Scripts/mathematics.py

echo "==> [3/5] Build paper + site pages"
python Scripts/build_paper.py

echo "==> [4/5] Export documents (PDF / DOCX / HTML)"
python Scripts/export_docs.py || echo "   (export step reported a problem; continuing)"

echo "==> [5/5] Build static site"
if command -v mkdocs >/dev/null 2>&1; then
  mkdocs build --clean
  echo "   site/ built."
else
  echo "   mkdocs not installed — skipping site build (run: pip install mkdocs-material)"
fi

echo "==> Done."
