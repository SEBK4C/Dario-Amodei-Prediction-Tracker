#!/usr/bin/env python3
"""Validate Mem/predictions.yaml against the schema.

Exit code 0 = clean, 1 = problems found. Wired into CI so a malformed or
unsupported prediction record fails the build before it can be published.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import dataio  # noqa: E402


def main() -> int:
    try:
        preds = dataio.load_predictions()
    except Exception as exc:  # noqa: BLE001 - surface any load error to CI
        print(f"FAILED to load predictions: {exc}", file=sys.stderr)
        return 1

    problems = dataio.validate(preds)
    print(f"Loaded {len(preds)} prediction(s) from {dataio.PREDICTIONS_FILE.name}")
    if problems:
        print(f"\n{len(problems)} validation problem(s):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print("Schema validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
