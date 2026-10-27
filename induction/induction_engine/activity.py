"""운동 종류 고르기: 주간 비율(R05), 날씨(R06), 상태·안전 허용 강도(R03·R04)."""
from .config import KINDS
from .history import completed, week_window
from .types import UserState


def weather_reason(cfg, weather):
    """실외 운동을 피해야 하면 이유 키(precipitation|cold|heat|dust), 아니면 None."""
    if weather is None:
        return None
    w = cfg["weather"]
    if weather.precipitation:
        return "precipitation"
    if weather.temp_c is not None and weather.temp_c < w["below_temp_c"]:
        return "cold"
    if weather.temp_c is not None and weather.temp_c >= w["heat_temp_c"]:
        return "heat"
    if (weather.pm10 is not None and weather.pm10 >= w["pm10_bad"]) or \
            (weather.pm25 is not None and weather.pm25 >= w["pm25_bad"]):
        return "dust"
    return None


def candidates(cfg, intensity, state, weather_key, fall_concern):
    out = []
    for a in cfg["activities"]:
        if intensity == "low" and a["intensity"] != "low":
            continue
        if state == UserState.FEAR and not a["seated"]:
            continue                        # 두려움 단계: 의자에 앉아서만
        if weather_key and not a["indoor"]:
            continue
        if fall_concern and not a["supported"]:
            continue                        # 낙상 걱정: 붙잡을 곳 있는 동작만
        out.append(a)
    return out


def pick_kind(cfg, history, today, fall_concern, available_kinds):
    """이번 주(최근 7일) 실적 대비 목표 비율에서 가장 모자란 종류."""
    weights = cfg["mix"]["fall_concern" if fall_concern else "default"]
    total_w = sum(weights.values())
    start, end = week_window(today)
    done = completed(history.sessions, start, end)
    n = len(done)
    deficit = {k: weights[k] / total_w * (n + 1) - sum(1 for s in done if s.kind == k) for k in KINDS}
    order = cfg["mix"]["tie_order"]
    pool = [k for k in order if k in available_kinds]
    return max(pool, key=lambda k: (round(deficit[k], 9), -order.index(k)))


def pick_activity(cfg, history, today, intensity, state, weather_key, fall_concern):
    pool = candidates(cfg, intensity, state, weather_key, fall_concern)
    kind = pick_kind(cfg, history, today, fall_concern, {a["kind"] for a in pool})
    in_kind = [a for a in pool if a["kind"] == kind]
    # 허용되면 보통 강도를 먼저, 같은 조건이면 최근에 덜 한 것(종류 다양화)
    last_used = {}
    for s in completed(history.sessions, end=today):
        last_used[s.activity_id] = max(last_used.get(s.activity_id, s.day), s.day)
    in_kind.sort(key=lambda a: (a["intensity"] != "moderate", last_used.get(a["id"]) or today.min,
                                cfg["activities"].index(a)))
    return in_kind[0]


def easier_activity(cfg, activity, weather_key, fall_concern):
    """'더 쉬운 걸로': 같은 종류의 앉아서 하는 저강도 동작."""
    pool = candidates(cfg, "low", UserState.FEAR, weather_key, fall_concern)
    same = [a for a in pool if a["kind"] == activity["kind"]]
    return (same or pool)[0]
