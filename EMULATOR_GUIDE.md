# 안드로이드 에뮬레이터로 운동친구 실행하기 (휴대폰 없이)

```
디즈먼트 워치 ──블루투스──▶ PC: watch_bridge.py ──ws://10.0.2.2:8765──▶ 에뮬레이터: 운동친구 앱
                           PC: dev_server.py   ──http://10.0.2.2:8000──▶        〃
```
- 에뮬레이터는 PC의 블루투스로 실제 워치에 붙을 수 없습니다. 그래서 **PC가 워치 심박을 받아 에뮬레이터 앱에 넘깁니다.**
- 에뮬레이터 안에서 `10.0.2.2` 는 PC 자신을 뜻합니다(설정 필요 없음).
- 워치 심박은 앱 안의 안전 엔진이 **B 등급(경고용)** 으로 판정합니다. 크게 넘어도 일시정지까지만, 끊기면 강도를 낮추고 질문을 늘립니다.

## 1. 준비 (한 번만)
1. **Android Studio** 설치 → Device Manager → 기기 만들기 (예: Pixel 7, Android 14/15 이미지). 실행해 두기.
2. **Python 3.10 이상**. 받은 폴더에서:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate            # Mac/Linux: source .venv/bin/activate
   pip install -e safety -e induction
   pip install "fastapi>=0.110" "sqlalchemy>=2.0" "uvicorn>=0.29" -r watch_bridge/requirements.txt
   ```

## 2. 실행 (터미널 두 개)
**터미널 1 — 서버**
```bash
python server/dev_server.py
```
로그인할 때 **인증번호가 이 터미널에 찍힙니다**(문자 대신).

**터미널 2 — 워치 브리지**
```bash
python watch_bridge/watch_bridge.py serve --simulate            # 워치 오기 전: 가상 워치
python watch_bridge/watch_bridge.py scan                        # 워치 온 뒤: 주소 찾기
python watch_bridge/watch_bridge.py inspect <주소>               #   표준 심박 서비스 확인
python watch_bridge/watch_bridge.py serve --address <주소>       #   실제 워치 중계
```
워치는 보통 한 번에 한 기기에만 붙습니다. 휴대폰의 워치 앱 연결은 끊어 두세요.

## 3. 앱 설치
PC 종류에 맞는 파일을 실행 중인 에뮬레이터 화면에 **끌어다 놓으면** 설치됩니다. (또는 `adb install <파일>`)
- Windows / 인텔·AMD 맥·리눅스: `운동친구_x86_64.apk`
- 애플 실리콘 맥(M1~M4): `운동친구_arm64.apk`

## 4. 앱에서
1. 휴대폰 번호 아무거나 → 터미널 1에 찍힌 인증번호 → 이름·태어난 해 → 건강 정보 동의 → 질문 몇 개
2. 홈 화면 **"워치 연결하기"** → "워치 연결됨 · 심박 ○○"
3. **"혈압 재고 시작하기"** → 운동 시작 → 운동 화면에 "디즈먼트 워치 (실시간)" 심박 카드
4. 가상 워치는 안정 → 상승 → **126** → 회복 → **30초 끊김**을 반복합니다. 126에서는 일시정지, 끊기면 "워치 신호가 끊겼어요" 안내가 나옵니다.

## 잘 안 될 때
| 증상 | 확인 |
|---|---|
| 로그인에서 멈춤 | 터미널 1 서버가 켜져 있는지 |
| "PC 워치 브리지에 연결하지 못했어요" | 터미널 2 브리지가 켜져 있는지(포트 8765) |
| "이 워치는 표준 심박 서비스가 없어요" | 이 워치는 블루투스로 심박을 직접 받을 수 없음 → 헬스 앱 경유 / 공급사 협력(계획서 7-3) |
| 심박이 몇십 초에 한 번만 옴 | 워치에서 운동(걷기) 모드를 켜 보기. `watch_bridge/records/hr_*.csv` 의 간격 확인 |

소스에서 바로 실행하려면(Flutter 설치 시): `cd mobile && flutter run --dart-define=ALLOW_DRAFT_RULES=true`
