# 운동친구 — 만성질환 어르신 운동 코치

만성질환 어르신이 혈압을 재면 **안전 규칙**이 오늘 운동을 정하고, **유도 규칙**이 작게 시작하도록 이끌고,
보호자에게는 어르신이 고른 만큼만 알리는 앱입니다. (외주 계획서 5·6·7장 구현)

| 폴더 | 내용 | 테스트 |
|---|---|---|
| `safety/` | 안전 엔진(Python 기준 구현) · 규칙 YAML · **정답표 352건** · 자문단 검토서 | `pytest` |
| `safety_dart/` | 같은 안전 엔진의 휴대폰용(Dart) 구현. 같은 정답표 통과 | `dart test` |
| `induction/` | 유도 엔진: 상태 4단계·운동 사다리·알림·재참여·문구 124개 | `pytest` |
| `server/` | FastAPI 서버: 회원·보호자·운동 기록·판정 로그(해시 체인)·규칙 배포·스케줄러 | `pytest` |
| `mobile/` | 어르신용 Flutter 앱(12개 화면, 안전 엔진 내장) | `flutter test` |
| `watch_bridge/` | 디즈먼트 워치(Diz-SW01) ↔ PC 블루투스 브리지, 가상 워치 | `pytest` |
| `demo/` | 서버 없이 열리는 HTML 시연(어르신·보호자 화면 나란히) | 브라우저 테스트 |
| `demo_video/` | 시연 영상 녹화 스크립트 | — |

## 빠르게 실행 (개발 서버 + 가상 워치 + 앱 화면)
```bash
python3 -m venv .venv
.venv/bin/pip install -e safety -e induction "fastapi>=0.110" "sqlalchemy>=2.0" "uvicorn>=0.29" -r watch_bridge/requirements.txt
.venv/bin/python server/dev_server.py                                   # 터미널 1 (인증번호가 여기 찍힘)
.venv/bin/python watch_bridge/watch_bridge.py serve --simulate          # 터미널 2
```
앱: `cd mobile && flutter run --dart-define=ALLOW_DRAFT_RULES=true` · 에뮬레이터 안내는 `EMULATOR_GUIDE.md`

## 전체 테스트
```bash
./run_all_tests.sh
```

## 지켜야 할 원칙
- **안전 판정은 규칙으로만.** 수치는 `safety/rules/safety_rules.yaml` 한 곳에만 있고, 바꾸면 정답표가 깨진다(자문단 승인 후에만 변경).
- 현재 규칙은 **draft(자문단 확정 전)** 입니다. 운영 배포 전 `docs/RULES.md`의 확인 항목을 자문단과 확정해야 합니다.
- 실제 건강 정보·개인 정보는 저장소에 올리지 않습니다(`.gitignore` 참고).
