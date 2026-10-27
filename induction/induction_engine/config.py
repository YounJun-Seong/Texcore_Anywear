"""유도 규칙·문구 풀·가드레일 로드와 검증."""
import copy
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

RULES_DIR = Path(__file__).resolve().parent.parent / "rules"
KINDS = ("aerobic", "strength", "balance")
PLACEHOLDERS = {"minutes", "activity", "goal", "reason"}


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class InductionConfig:
    rules: dict
    messages: tuple          # ({id, intent, text}, ...)
    guardrails: dict         # category -> [compiled regex]
    version: str
    sha256: str

    def __getitem__(self, key):
        return self.rules[key]

    def activity(self, activity_id):
        return next(a for a in self.rules["activities"] if a["id"] == activity_id)


def _load(name):
    with open(RULES_DIR / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config(rules=None, messages=None, guardrails=None):
    rules = copy.deepcopy(rules if rules is not None else _load("induction_rules.yaml"))
    messages = copy.deepcopy(messages if messages is not None else _load("messages.yaml"))
    guardrails = copy.deepcopy(guardrails if guardrails is not None else _load("guardrails.yaml"))
    validate(rules, messages)
    compiled = {cat: [re.compile(p) for p in pats] for cat, pats in guardrails["categories"].items()}
    canonical = json.dumps([rules, messages, guardrails], ensure_ascii=False, sort_keys=True)
    return InductionConfig(rules=rules, messages=tuple(messages), guardrails=compiled,
                           version=str(rules["meta"]["version"]),
                           sha256=hashlib.sha256(canonical.encode("utf-8")).hexdigest())


def _require(cond, msg):
    if not cond:
        raise ConfigError(msg)


def validate(r, messages):
    lad = r["ladder"]
    steps = lad["steps_minutes"]
    _require(steps == sorted(steps) and len(set(steps)) == len(steps), "ladder steps must strictly increase")
    _require(steps[-1] <= lad["daily_cap_minutes"], "top ladder step exceeds daily cap")
    _require(0 < lad["weekly_increase_max"] <= 0.10, "weekly increase must be in (0, 10%]")
    _require(lad["mini_session_minutes"] < steps[0], "mini session must be shorter than first step")
    _require(r["notifications"]["max_per_day"] <= 2, "at most 2 notifications per day")
    _require(r["notifications"]["reduced_max_per_day"] < r["notifications"]["max_per_day"], "reduced must be lower")

    ids = [a["id"] for a in r["activities"]]
    _require(len(ids) == len(set(ids)), "duplicate activity id")
    for kind in KINDS:
        # 어떤 조건(노랑·두려움·날씨)에서도 고를 것이 남도록 종류마다 앉아서 하는 실내 저강도가 있어야 한다.
        _require(any(a["kind"] == kind and a["intensity"] == "low" and a["indoor"] and a["seated"]
                     for a in r["activities"]), f"{kind}: needs a seated indoor low-intensity activity")
    for mix in ("default", "fall_concern"):
        _require(set(r["mix"][mix]) == set(KINDS), f"mix.{mix} must cover {KINDS}")

    tiers = [t["from"] for t in r["reengagement"]["tiers"]]
    _require(tiers == sorted(tiers), "reengagement tiers must be ordered")
    _require(tiers[-1] == lad["restart_missed_days"], "last tier must match restart_missed_days")

    mids = [m["id"] for m in messages]
    _require(len(mids) == len(set(mids)), "duplicate message id")
    for m in messages:
        used = set(re.findall(r"{(\w+)}", m["text"]))
        _require(used <= PLACEHOLDERS, f"{m['id']}: unknown placeholder {used - PLACEHOLDERS}")
