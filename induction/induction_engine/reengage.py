"""이탈 방지·재참여 사다리(6-4: R15). 보호자·담당자 행동은 어르신 동의와 공유 범위 안에서만."""
from .history import missed_days


def _allowed(requirements, profile):
    return all(getattr(profile, k) == v for k, v in requirements.items())


def reengagement(cfg, profile, history, today):
    """
    반환: {missed_days, tier, actions, withheld}
    actions는 해당 단계에 처음 들어선 날에만 나온다(매일 반복하지 않음).
    withheld: 동의·공유 범위 때문에 하지 않은 행동(로그용).
    """
    r = cfg["reengagement"]
    missed = missed_days(history.sessions, profile.signup_date, today)
    tier = None
    for t in r["tiers"]:
        if missed >= t["from"]:
            tier = t
    if tier is None:
        return {"missed_days": missed, "tier": None, "actions": [], "withheld": []}
    actions, withheld = [], []
    if missed == tier["from"]:
        for a in tier["actions"]:
            (actions if _allowed(r["requires"].get(a, {}), profile) else withheld).append(a)
    return {"missed_days": missed, "tier": tier["code"], "actions": actions, "withheld": withheld}
