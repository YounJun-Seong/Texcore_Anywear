# 유도 엔진 (계획서 6장)

"어떻게 하게 만들 것인가". 안전 엔진(`../safety`)이 허용한 범위 안에서만 오늘의 운동·알림·문구를 고른다.
MVP는 규칙 기반 JITAI(결정 규칙 17개, `docs/RULES.md`)이고, 2차 맥락적 밴딧은 같은 후보 목록 안에서만 고르도록 붙이면 된다.

```
rules/induction_rules.yaml   사다리·상태·비율·날씨·알림·재참여 수치
rules/messages.yaml          문구 풀 124개(발주사 검수 필요)
rules/guardrails.yaml        금지 표현(의료 주장·보장·죄책감·위협·외래어·유아 말투)
induction_engine/
  state.py      사용자 상태 4단계          ladder.py   운동 사다리, 하루·주간 상한
  activity.py   운동 종류·날씨 전환         notify.py   알림 시각·개수·피로
  reengage.py   이탈 방지 사다리            rewards.py  도장·연속 일수
  messages.py   문구 고르기(14일 반복 금지)   guardrails.py  문구 검사, AI 입력 축소
  planner.py    plan_today (안전 엔진 결과 → 오늘 계획)
```

## 실행
```bash
cd ../safety && python3 -m venv --without-pip .venv && python3 -m pip --python .venv/bin/python install -r requirements.txt
cd ../induction && ../safety/.venv/bin/python -m pytest -q tests
```

## 하루 흐름
```python
from induction_engine import *
from safety_engine import load_rules, Profile, Vitals
from safety_engine.precheck import pre_check

cfg, srules = load_config(), load_rules()
ladder, code = ladder_update(cfg, ladder, history, user.signup_date, today)   # 아침 첫 진입
notes = plan_notifications(cfg, user, history, today, ladder.level)           # 오늘 알림(최대 2개)
decision = pre_check(srules, health_profile, Vitals(...), symptoms)           # 혈압 입력 = 앵커
plan = plan_today(cfg, srules, user, ladder, history, decision, today, weather)
# plan.action, plan.minutes, plan.activity_id, plan.easier, plan.message.text, plan.rules_fired
# 운동 후: completion_message(...), day_reward(...), reengagement(...)는 매일 서버 스케줄러에서
```
모든 함수는 순수 함수다(시계·DB 조회 없음). 기록 저장과 알림 발송은 서버가 맡는다.
