import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "safety"))

from induction_engine import History, SessionRecord, load_config  # noqa: E402
from safety_engine import load_rules  # noqa: E402

D0 = date(2026, 10, 1)


def day(n):
    return D0 + timedelta(days=n)


_CFG = load_config()


def sess(n, level=0, kind="aerobic", minutes=None, activity_id=None, completed=True, **kw):
    steps = _CFG["ladder"]["steps_minutes"]
    default_activity = {"aerobic": "chair_march", "strength": "chair_strength", "balance": "chair_balance"}[kind]
    return SessionRecord(day=day(n), completed=completed, minutes=steps[level] if minutes is None else minutes,
                         level=level, kind=kind, activity_id=activity_id or default_activity, **kw)


def hist(sessions=(), prechecks=(), notifications=(), messages=()):
    return History(tuple(sessions), tuple(prechecks), tuple(notifications), tuple(messages))


@pytest.fixture(scope="session")
def cfg():
    return _CFG


@pytest.fixture(scope="session")
def srules():
    return load_rules()
