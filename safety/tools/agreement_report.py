"""엔진 판정 vs 정답표 일치율 (검수 기준: 98% 이상, 계획서 5-5·11-2).

의료 자문단이 scenarios/ 사본의 expected 열을 직접 고쳐서 넘기면 그 폴더를 지정한다.

    python tools/agreement_report.py                       # 기본 정답표
    python tools/agreement_report.py --answers advisor_v1/  # 자문단 정답표
    python tools/agreement_report.py --rules rules/safety_rules.yaml --threshold 0.98
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from safety_engine.rules import DEFAULT_RULES_PATH, load_rules  # noqa: E402
from scenario_runner import SCENARIO_DIR, SUITES, load_suite  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", default=str(SCENARIO_DIR))
    ap.add_argument("--rules", default=str(DEFAULT_RULES_PATH))
    ap.add_argument("--threshold", type=float, default=0.98)
    args = ap.parse_args()

    rules = load_rules(args.rules)
    print(f"규칙 {rules.version} ({rules.sha256[:12]}), 상태: {rules['meta']['status']}")
    total = agree = 0
    mismatches = []
    for name in SUITES:
        path = Path(args.answers) / name
        if not path.exists():
            print(f"  {name}: 없음(건너뜀)")
            continue
        rows, runner = load_suite(name, args.answers)
        ok_count = 0
        for row in rows:
            try:
                ok, got = runner(rules, row)
            except Exception as e:  # 정답표 입력 오류도 불일치로 센다
                ok, got = False, f"오류: {e}"
            ok_count += ok
            if not ok:
                mismatches.append((row["id"], row.get("note") or row.get("desc"), row.get("expected"), got))
        total += len(rows)
        agree += ok_count
        print(f"  {name}: {ok_count}/{len(rows)}")

    rate = agree / total if total else 0.0
    print(f"\n전체 일치율 {agree}/{total} = {rate:.2%} (기준 {args.threshold:.0%})")
    for sid, note, expected, got in mismatches:
        print(f"  ✗ {sid} {note}\n      정답: {expected}\n      엔진: {got}")
    passed = total >= 300 and rate >= args.threshold
    print("검수 통과" if passed else "검수 미통과")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
