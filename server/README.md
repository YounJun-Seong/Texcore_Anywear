# 서버 (계획서 7장)

FastAPI 서버. 회원·보호자·운동 기록 API, 판정 로그 저장, 단말용 안전 규칙 번들 배포, 하루 스케줄러를 맡는다.
판정은 `../safety`, 유도는 `../induction` 엔진이 하고 서버는 기록·연결·알림만 한다.

## 실행
```bash
cd senior_exercise_app
python3 -m venv --without-pip .venv && python3 -m pip --python .venv/bin/python install -r server/requirements.txt
cd server
ALLOW_DRAFT_RULES=1 ../.venv/bin/uvicorn app.main:create_app --factory --reload   # http://localhost:8000/docs
../.venv/bin/python -m pytest -q tests
```
운영 cron: `python -m app.cli daily`(매일 06:30), `python -m app.cli dispatch`(5분마다), 관리자 생성 `python -m app.cli create-admin <번호> <이름>`.

## API 한눈에
| 누가 | 경로 | 하는 일 |
|---|---|---|
| 모두 | `POST /auth/otp/request`, `/auth/otp/verify` | 휴대폰 문자 인증 → 토큰. 처음이면 가입(어르신·보호자) |
| 어르신 | `POST /me/consents`, `PUT /me/health`, `PUT /me/settings` | 항목별 동의(이력 저장·철회), 건강 정보(동의 필수), 알림 시간·목표 |
| 어르신 | `GET /me/today` | 오늘 처리(사다리·알림 예약·재참여)를 실행하고 상태·도장·응원 여부 |
| 어르신 | `POST /me/prechecks` | 운동 전 점검 → **안전 엔진** 판정 → **유도 엔진** 오늘의 계획. 119 증상이면 보호자 전원 전화+푸시 |
| 어르신 | `POST /me/sessions` | 오늘 판정이 초록·노랑일 때만 시작. 분·운동은 계획에서만, 심박 상한 내려줌 |
| 어르신 | `POST /me/sessions/{id}/events` | 단말 안전 엔진이 낸 행동을 판정 로그에. 3분 무응답이면 보호자 알림 |
| 어르신 | `POST /me/sessions/{id}/finish` | 운동 후 회복 판정, 남은 알림 취소, 칭찬·도장, 보호자 응원 재생, "오늘 운동했어요"(공유 범위 전체만) |
| 어르신 | `POST /me/emergency` | 단말 응급 흐름 결과. 위치는 동의 시 전송만, 저장 안 함 |
| 어르신 | `GET /me/week`, `GET/PUT /me/guardians`, `DELETE /me/health-data` | 이번 주 기록, 보호자 수락·공유 범위·끊기, 건강 정보 삭제 |
| 보호자 | `POST /guardian/links`, `POST /guardian/elders` | 연결 요청(어르신 수락 필요) / 대리 설정(응급 공유만으로 시작) |
| 보호자 | `GET /guardian/elders/{id}/summary`, `GET /guardian/alerts`, `POST .../cheers` | 공유 범위만큼 요약(열람 로그), 알림, 응원 글·음성 |
| 단말 | `GET /rules/safety` | 승인된 규칙 번들(ETag). draft는 `ALLOW_DRAFT_RULES=1`일 때만 |
| 관리자 | `/admin/decision-log`, `/verify`, `/alerts`, `/jobs/daily`, `/jobs/dispatch` | 안전 이벤트 조회, 로그 무결성, 담당자 연계 대기, 스케줄러 수동 실행 |

## 보호자 공유 범위 (어르신이 고름, 기본 = 응급만)
| | 응급 알림 | 응원 보내기 | 오늘 했는지·주간 요약·이탈 알림·응원 요청 |
|---|---|---|---|
| emergency_only | O | X | X |
| cheer_only | O | O | X |
| full | O | O | O |

## 판정 로그
`decision_log`는 안전 엔진 파일 로그와 같은 해시 체인. ORM 수정·삭제는 예외를 던지고, DB를 직접 고쳐도 `/admin/decision-log/verify`가 위치를 찾는다.
운영 PostgreSQL에서는 앱 계정에 이 테이블 INSERT·SELECT만 준다. 체인 끝은 `decision_log_head` 한 행을 `FOR UPDATE`로 잠가 동시 기록에도 순서를 지킨다.

## 아직 아닌 것 (운영 전 필요)
- **게이트웨이**: 지금은 메모리 기록(`MemoryGateway`). FCM 푸시·문자·음성 전화 사업자 구현 필요.
- **PostgreSQL 검증·마이그레이션**: 테스트는 SQLite. Alembic 스키마 관리와 국내 리전 DB 저장 암호화 설정 필요.
- **보건소·복지관 담당자** 계정 모델이 없어 14일 이탈 시 담당자 전화 권유(`manager_call`)는 아직 나가지 않음.
- **날씨**: 기상청·에어코리아 연결부(`weather`) 자리만 있음.
- 인증번호 요청 횟수 제한, 단말이 보낸 운동 중 기록을 서버에서 다시 재생해 검증하는 기능.
