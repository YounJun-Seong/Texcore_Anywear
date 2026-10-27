# 디즈먼트 워치 ↔ 시연 HTML 연결 (파이썬 브리지)

워치 → (블루투스) → **내 컴퓨터의 `watch_bridge.py`** → (ws://localhost:8765) → **시연 HTML 파일**

시연 HTML 안의 안전 엔진이 워치 심박을 **B 등급(경고용)** 으로 판정합니다. 크게 넘어도 중단이 아니라 일시정지까지만 가고,
숨찬 정도 질문을 함께 합니다. 심박이 15초 넘게 안 오면 "심박 끊김"으로 보고 강도를 낮추고 질문을 늘립니다.

## 준비 (블루투스가 있는 노트북·PC, Windows / Mac / Linux)
```bash
pip install -r requirements.txt        # bleak, websockets
```
- 워치는 **한 번에 한 기기에만** 붙는 경우가 많습니다. 시험 전에 휴대폰의 워치 앱(SMART-TIME PRO 등) 연결을 끊거나 휴대폰 블루투스를 꺼 두세요.
- 시연은 **받은 HTML 파일(운동친구_시연.html)을 브라우저로 열어서** 하세요. claude.ai 링크에서는 보안 정책 때문에 내 컴퓨터(localhost)로 연결이 막힙니다.

## 워치 오기 전: 가상 워치로 연결 시험
```bash
python watch_bridge.py serve --simulate
```
HTML 파일을 열고 조작 영역의 **"내 컴퓨터 워치 연결"** 을 누르면 가상 심박(안정 → 상승 → 126 → 회복 → 30초 끊김)이 들어옵니다.

## 워치 온 날: 3단계
```bash
python watch_bridge.py scan                    # 1) 주변 기기 찾기 — '워치일 수 있음' 표시와 주소 확인
python watch_bridge.py inspect <주소>           # 2) 표준 심박 서비스가 있는지 확인 (결과는 records/inspect_*.json)
python watch_bridge.py serve --address <주소>   # 3) 있으면 HTML로 중계 시작
```
- 2)에서 **"표준 심박 서비스가 없습니다"** 가 나오면, 이 워치는 블루투스로 심박을 직접 받을 수 없습니다(계획서 7-3 B안 불가).
  이때는 헬스 앱 경유(A안)나 공급사 협력(C안)으로 갑니다. 제조사 허락 없이 비공개 통신 규격을 분석하지 않습니다.
- 운동 모드를 켜야 심박을 보내는 워치도 있습니다. 심박이 안 들어오면 워치에서 운동(걷기)을 시작해 보세요.
- 받은 심박은 `records/hr_*.csv` 에 시각·심박·간격으로 남습니다. 전송 간격과 끊김은 PoC-0 점검표의 "심박 전송 주기·연결 안정성" 근거가 됩니다.

## 시험
```bash
python -m pytest -q test_watch_bridge.py       # 심박 패킷 해석·기록
```
