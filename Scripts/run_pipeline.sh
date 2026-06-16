#!/usr/bin/env bash
# Reproducible end-to-end pipeline for the Dario Amodei Prediction Tracker.
# 1) test the acceleration thesis  2) generate the paper  3) build the site.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== [1/3] Thesis testing =="
python3 Scripts/thesis_acceleration.py
echo "== [2/3] Paper generation =="
python3 Scripts/generate_paper.py
echo "== [3/3] Static site build =="
python3 Scripts/build_site.py
echo "== Pipeline complete =="
