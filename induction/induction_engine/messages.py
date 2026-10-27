"""문구 고르기(R14): 같은 문구는 14일 안에 다시 쓰지 않는다."""
import re

from .guardrails import violations
from .types import Message


class MessageError(ValueError):
    pass


def render(text, values):
    return re.sub(r"{(\w+)}", lambda m: str(values[m.group(1)]), text)


def _needs(text):
    return set(re.findall(r"{(\w+)}", text))


def pick_message(cfg, intent, used, today, values=None, exclude=()):
    """
    used: MessageUse 목록(최근 사용 이력). exclude: 같은 날 이미 고른 id.
    반환: (Message, 사유 코드)
    """
    values = {k: v for k, v in (values or {}).items() if v is not None}
    pool = [m for m in cfg.messages if m["intent"] == intent and _needs(m["text"]) <= set(values)]
    if not pool:
        raise MessageError(f"no message for intent {intent} with values {sorted(values)}")

    window = cfg["notifications"]["no_repeat_days"]
    last_used = {}
    for u in used:
        if u.day <= today:
            last_used[u.message_id] = max(last_used.get(u.message_id, u.day), u.day)
    blocked = {mid for mid, day in last_used.items() if (today - day).days < window} | set(exclude)

    fresh = [m for m in pool if m["id"] not in blocked]
    code = "MSG_FRESH"
    if not fresh:
        # 풀이 모자라면 가장 오래전에 쓴 것을 다시 쓴다(풀 확장 필요 신호로 로그에 남김)
        fresh = [m for m in pool if m["id"] not in set(exclude)] or pool
        code = "MSG_REPEAT_FALLBACK"
    choice = min(fresh, key=lambda m: (last_used.get(m["id"]) or today.min, m["id"]))

    text = render(choice["text"], values)
    bad = violations(cfg, text)
    if bad:
        raise MessageError(f"{choice['id']} fails guardrails: {bad}")
    return Message(id=choice["id"], intent=intent, text=text), code
