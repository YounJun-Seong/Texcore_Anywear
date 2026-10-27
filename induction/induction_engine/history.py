"""기록 집계 도우미. 주(week)는 오늘을 끝으로 하는 7일 구간으로 센다(달력 주 아님)."""
from datetime import timedelta

BAD_LIGHTS = {"RED", "EMERGENCY"}


def completed(sessions, start=None, end=None):
    return [s for s in sessions if s.completed
            and (start is None or s.day >= start) and (end is None or s.day <= end)]


def week_window(today, weeks_back=0):
    end = today - timedelta(days=7 * weeks_back)
    return end - timedelta(days=6), end


def count_in_week(sessions, today, weeks_back=0):
    start, end = week_window(today, weeks_back)
    return len(completed(sessions, start, end))


def minutes_in(sessions, start, end):
    return sum(s.minutes for s in completed(sessions, start, end))


def last_completed_day(sessions, today):
    days = [s.day for s in completed(sessions, end=today)]
    return max(days) if days else None


def missed_days(sessions, signup_date, today):
    """오늘을 빼고, 마지막 운동 다음 날부터 어제까지 연속으로 안 한 날 수."""
    ref = last_completed_day(sessions, today) or (signup_date - timedelta(days=1))
    return max(0, (today - ref).days - 1)
