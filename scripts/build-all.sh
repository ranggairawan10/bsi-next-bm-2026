#!/bin/bash
# Build all 8 HTML files dari Python source.
# Usage: bash build-all.sh
set -e
cd "$(dirname "$0")"
echo "==== Building BSI Scoring System v2 ===="
for f in build_*.py; do
  echo ""
  echo "→ $f"
  python3 "$f"
done
echo ""
echo "==== Build Complete ===="
ls -la ../bsi-scoring/*.html
