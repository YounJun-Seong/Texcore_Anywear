# 안전 엔진 (계획서 5장)

어르신 운동 앱의 **운동 전·중·후 안전 판정**. 규칙 기반(결정론적)이고, 수치는 전부 버전이 붙은 규칙 파일에 있다.
같은 규칙 번들을 서버와 단말(오프라인 동작)이 함께 쓴다. 이 폴더는 Python 기준 구현이자 정답표다.
단말(Flutter/RN) 포팅은 같은 `scenarios/`를 통과해야 한다.

```
rules/safety_rules.yaml      규칙 번들(수치의 유일한 출처, draft → 자문단 승인 후 approved)
safety_engine/
  precheck.py                하드 게이트(5-1), 운동 전 신호등(5-2), 허용 범위, 운동 후 회복
  session.py                 심박 상한 계산, 운동 중 모니터(5-3)
  emergency.py               응급 흐름 상태 기계(5-4)
  audit_log.py               해시 체인 판정 로그(입력→판정→사유 코드+규칙 버전)
  engine.py                  앱·서버 진입점(모든 판정을 로그에 남김)
scenarios/                   정답표 352건(CSV는 엑셀로 열어 자문단이 수정 가능). 단말 Dart 엔진(../safety_dart)도 같은 표를 통과해야 함
tools/agreement_report.py    엔진 vs 정답표 일치율(검수 기준 98%)
tools/export_bundle.py       단말 배포용 JSON(승인된 번들만)
tools/generate_scenarios.py  정답표 초안 생성(계획서 표를 따로 옮겨 적음, YAML을 읽지 않음)
docs/RULES.md                자문단 검토서(확인 필요 항목 13개 포함)
```

## 실행
```bash
python3 -m venv --without-pip .venv && python3 -m pip --python .venv/bin/python install -r requirements.txt
.venv/bin/python -m pytest -q tests
.venv/bin/python tools/agreement_report.py
```

## 사용 예
```python
from safety_engine import SafetyEngine, Profile, Vitals, DoctorLimits
from safety_engine.audit_log import DecisionLog

eng = SafetyEngine(log=DecisionLog("decisions.jsonl"))
p = Profile(age=74, beta_blocker=False)
d = eng.pre_check(p, Vitals(165, 85, 72, bp_source="ble_upper_arm"), symptoms=["mild_fatigue"])
d.outcome, d.reasons            # 'YELLOW', ('PRE_YELLOW_SYMPTOM', 'PRE_SBP_ELEVATED', ...)
eng.allowance(d.outcome, 10)    # {'allowed': True, 'max_minutes': 5, 'intensity': 'low', ...}

limits, mon = eng.start_session(p, hr_grade="A", light=d.outcome)
mon.on_hr(t=12, bpm=118)        # 1초마다 tick(t)/on_hr(t, bpm), 사용자 답은 on_rpe/on_symptom/on_user_stop
```

## 원칙
- 규칙 수치를 바꾸면 정답표가 깨진다(`tests/test_rules.py`가 확인). 수치 변경 = 자문단 승인 + 정답표 수정 + 버전 올림.
- 모르는 증상·출처 이름은 조용히 무시하지 않고 오류를 낸다.
- 애매하면 안전한 쪽: 빨강 > 재측정, 워치 심박은 좋게 나와도 근거로 안 씀, 센서 끊기면 강도를 낮추고 더 자주 묻는다.
