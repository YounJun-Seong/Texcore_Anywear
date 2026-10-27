#!/usr/bin/env bash
# 전체 테스트: 안전(Python) → 유도 → 서버 → 안전(Dart, 같은 정답표) → 앱
set -euo pipefail
cd "$(dirname "$0")"
export PATH="$HOME/flutter/bin:$PATH"
for d in safety induction server; do (cd $d && echo "== $d" && ../.venv/bin/python -m pytest -q tests | tail -1); done
(cd safety && ../.venv/bin/python tools/agreement_report.py | tail -2)
(cd safety_dart && echo "== safety_dart" && dart test 2>&1 | tail -1)
(cd mobile && echo "== mobile" && flutter analyze | tail -1 && flutter test 2>&1 | tail -1)
