"""사용자 상태 4단계(6-1)."""
from datetime import timedelta

from .history import completed, count_in_week, last_completed_day
from .types import UserState


def _habit_at(cfg, sessions, day):
    s = cfg["states"]
    return all(count_in_week(sessions, day, k) >= s["habit_sessions_per_week"] for k in range(s["habit_weeks"]))


def habit_formed(cfg, sessions, signup_date, today):
    """가입 이후 어느 시점에든 '주 3회 이상 3주 연속'을 달성한 적이 있는가."""
    day = signup_date
    while day <= today:
        if _habit_at(cfg, sessions, day):
            return True
        day += timedelta(days=1)
    return False


def classify_state(cfg, sessions, signup_date, today):
    """
    판정 순서(R04 근거):
      1. 습관이 생긴 적 있고 마지막 운동 뒤 3일 이상 공백 → 이탈 위험
      2. 최근 3주 모두 주 3회 이상 → 습관
      3. 완료 2회 이하 → 두려움·무관심 (가입 2주가 지나도 2회 이하면 유지)
      4. 그 외 → 시작
    """
    s = cfg["states"]
    last = last_completed_day(sessions, today)
    if last is not None and (today - last).days >= s["lapse_gap_days"] and habit_formed(cfg, sessions, signup_date, today):
        return UserState.LAPSE_RISK
    if _habit_at(cfg, sessions, today):
        return UserState.HABIT
    if len(completed(sessions, end=today)) <= s["fear_max_completed"]:
        return UserState.FEAR
    return UserState.STARTING
