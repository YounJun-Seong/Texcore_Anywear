"""단말 배포용 규칙 번들(JSON) 만들기. 승인된 번들만 내보낸다(--allow-draft는 개발용).

    python tools/export_bundle.py --out build/safety_rules.json --allow-draft
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from safety_engine.rules import DEFAULT_RULES_PATH, load_rules  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", default=str(DEFAULT_RULES_PATH))
    ap.add_argument("--out", required=True)
    ap.add_argument("--allow-draft", action="store_true")
    args = ap.parse_args()

    rules = load_rules(args.rules, require_approved=not args.allow_draft)
    envelope = {"version": rules.version, "sha256": rules.sha256, "rules": rules.data}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{out}: {rules.version} {rules.sha256}")


if __name__ == "__main__":
    main()
