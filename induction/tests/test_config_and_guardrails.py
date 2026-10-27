import copy
import re

import pytest

from induction_engine import accept_generated, llm_brief, load_config, plan_today, violations
from induction_engine.config import ConfigError, _load
from induction_engine.messages import render
from induction_engine.types import LadderState, UserProfile
from safety_engine import Profile, Vitals
from safety_engine.precheck import pre_check

from conftest import D0, day, hist

SAMPLE = {"minutes": 5, "activity": "의자에 앉아 제자리 걷기", "goal": "손주 안아주기", "reason": "비가 와서"}
CODE_INTENTS = {"today_FEAR", "today_STARTING", "today_HABIT", "today_LAPSE_RISK", "today_yellow", "today_weather",
                "rest_red", "remeasure", "doctor_check", "done_for_today", "complete", "complete_goal", "level_up",
                "level_down", "reminder", "reminder_bp", "evening_mini", "ask_reason", "cause_check",
                "restart_offer", "ask_time_change"}


def test_pool_size_meets_launch_requirement(cfg):
    assert len(cfg.messages) >= 100


def test_every_intent_used_by_engine_has_messages(cfg):
    assert CODE_INTENTS <= {m["intent"] for m in cfg.messages}


@pytest.mark.parametrize("mid", [m["id"] for m in load_config().messages])
def test_every_message_passes_guardrails_when_rendered(cfg, mid):
    m = next(x for x in cfg.messages if x["id"] == mid)
    text = render(m["text"], SAMPLE)
    assert violations(cfg, text) == [], text


@pytest.mark.parametrize("text,category", [
    ("이 운동으로 고혈압이 치료됩니다.", "medical_claim"),
    ("혈압이 내려갑니다.", "medical_claim"),
    ("이제 약을 줄이셔도 돼요.", "medical_claim"),
    ("위험하면 저희가 감지해 드립니다.", "guarantee"),
    ("100% 안전해요.", "guarantee"),
    ("왜 안 하셨어요?", "guilt"),
    ("또 안 하셨네요.", "guilt"),
    ("안 하시면 큰일 납니다.", "threat"),
    ("오늘 유산소 10분!", "jargon"),
    ("심박수를 확인하세요.", "jargon"),
    ("근력 운동 시간이에요.", "jargon"),
    ("오늘의 미션 완료", "jargon"),
    ("Good job!", "jargon"),
    ("옳지, 잘했어요~", "infantilizing"),
    ("{minutes}분이에요", "unresolved"),
])
def test_guardrails_catch(cfg, text, category):
    assert category in {c for c, _ in violations(cfg, text)}


def test_generated_text_falls_back_to_template(cfg):
    assert accept_generated(cfg, "오늘은 앉아서 5분만 해요.", "원문")[:2] == ("오늘은 앉아서 5분만 해요.", True)
    text, used, bad = accept_generated(cfg, "운동하면 혈압이 내려갑니다.", "원문")
    assert (text, used) == ("원문", False) and bad
    assert accept_generated(cfg, "", "원문")[:2] == ("원문", False)


def test_llm_brief_has_no_vitals_name_or_goal(cfg, srules):
    profile = UserProfile(signup_date=D0, goal="손주 안아주기")
    d = pre_check(srules, Profile(age=74), Vitals(147, 93, 88))
    plan = plan_today(cfg, srules, profile, LadderState(2, D0), hist(), d, day(1))
    brief = llm_brief(cfg, plan)
    flat = str({k: v for k, v in brief.items() if k != "template"})
    assert not re.search(r"147|93|88|손주", flat)
    assert set(re.findall(r"\d+", flat)) <= {str(plan.minutes)}


@pytest.mark.parametrize("mutate,msg", [
    (lambda r, m: r["ladder"].update(steps_minutes=[3, 5, 5, 8]), "strictly increase"),
    (lambda r, m: r["ladder"].update(steps_minutes=[3, 5, 90]), "daily cap"),
    (lambda r, m: r["ladder"].update(weekly_increase_max=0.2), "weekly increase"),
    (lambda r, m: r["notifications"].update(max_per_day=3), "at most 2"),
    (lambda r, m: r.update(activities=[a for a in r["activities"] if a["id"] != "chair_balance"]), "balance"),
    (lambda r, m: m.append({"id": "zz", "intent": "complete", "text": "{name}님"}), "placeholder"),
    (lambda r, m: m.append({"id": "c01", "intent": "complete", "text": "중복"}), "duplicate message"),
])
def test_invalid_config_rejected(mutate, msg):
    rules, messages = copy.deepcopy(_load("induction_rules.yaml")), copy.deepcopy(_load("messages.yaml"))
    mutate(rules, messages)
    with pytest.raises(ConfigError, match=msg):
        load_config(rules, messages)
