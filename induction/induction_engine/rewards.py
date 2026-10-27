"""보상(6-5: R16). '시작했다'·'혈압을 쟀다'·'빨강 날 쉬었다'에 준다. 운동량에 비례하지 않는다(과운동 방지)."""
from datetime import timedelta

from .history import week_window


def day_reward(history, day):
    reasons = []
    if any(s.day == day for s in history.sessions):
        reasons.append("SESSION_STARTED")
    checks = [p for p in history.prechecks if p.day == day]
    if checks:
        reasons.append("BP_MEASURED")
    if any(p.light == "RED" for p in checks):
        reasons.append("RESTED_ON_RED")
    return {"stamp": bool(reasons), "reasons": reasons}


def streak(history, today):
    """연속 도장 일수. 오늘 아직 도장이 없으면 어제까지로 센다(오늘 하루를 실패로 보지 않음)."""
    day = today if day_reward(history, today)["stamp"] else today - timedelta(days=1)
    n = 0
    while day_reward(history, day)["stamp"]:
        n += 1
        day -= timedelta(days=1)
    return n


def weekly_stamps(history, today):
    start, _ = week_window(today)
    return sum(day_reward(history, start + timedelta(days=i))["stamp"] for i in range(7))
