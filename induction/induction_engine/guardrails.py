"""문구 가드레일과 생성형 AI 연결부.

생성형 AI는 규칙이 정한 의도를 문장으로 다듬기만 한다(원칙 2). 그래서
  - AI에 보내는 입력은 범주뿐: 이름·목표·혈압·심박 숫자를 넣지 않는다(7-1).
  - AI가 돌려준 문장은 가드레일을 통과해야 쓰고, 아니면 검수된 원문을 쓴다.
"""
from .types import Plan

LIGHT_WORDS = {"GREEN": "평소대로", "YELLOW": "가볍게"}
KIND_WORDS = {"aerobic": "걷기·제자리 걷기", "strength": "힘 기르기", "balance": "균형 잡기"}


def violations(cfg, text):
    return [(cat, rx.pattern) for cat, patterns in cfg.guardrails.items() for rx in patterns if rx.search(text)]


def accept_generated(cfg, generated, fallback):
    """AI 문장이 깨끗하면 그대로, 아니면 원문 템플릿. (문장, 사용 여부, 위반 목록)"""
    bad = violations(cfg, generated or "")
    if generated and not bad:
        return generated, True, []
    return fallback, False, bad


def llm_brief(cfg, plan: Plan):
    """문장 다듬기용 입력. 수치 판단 재료(혈압·심박)·개인 식별 정보는 넣지 않는다."""
    brief = {"intent": plan.message.intent if plan.message else None, "action": plan.action,
             "tone": "존댓말, 짧게, 생활 언어, 아이 달래는 말투 금지"}
    if plan.action == "EXERCISE":
        activity = cfg.activity(plan.activity_id)
        brief.update(today=LIGHT_WORDS.get(plan.light, "쉬는 날"), activity=KIND_WORDS[activity["kind"]],
                     seated=activity["seated"], minutes=f"{plan.minutes}분")
    if plan.message:
        brief["template"] = plan.message.text
    return brief
