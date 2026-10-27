# 운동친구 시연 페이지

서버 없이 브라우저에서 열리는 보여주기용 데모. 어르신 화면·보호자 화면·판정 기록을 나란히 둔다.

- **판정은 진짜**: `../safety_dart` 안전 엔진을 `dart compile js`로 JS로 바꿔 넣었다(`engine.js`).
  넣기 전에 정답표 352건을 브라우저에서 돌려 모두 일치하는지 확인한다(`tests/engine_parity.py`).
- **간단히 흉내 낸 것**: 운동 종류·시간 고르기(유도 엔진), 보호자 알림 전달, 연속 일수. 실제는 서버가 한다.

## 다시 만들기
```bash
cd ../safety_dart && dart compile js -O2 -o ../demo/engine.js web/bridge.dart && rm -f ../demo/engine.js.*
cd ../demo && ../.venv/bin/python build.py                      # → dist/index.html (파일 하나)
../.venv/bin/python tests/engine_parity.py                      # 컴파일된 엔진 = 정답표 352건
../.venv/bin/python tests/demo_flows.py /tmp/shots              # 상황 6개 끝까지, 가로 넘침·콘솔 오류 검사
```
테스트는 헤드리스 Chromium(playwright)이 필요하다. 이 서버에서는 시스템을 건드리지 않으려고 필요한 라이브러리를
임시 폴더에 풀어 `LD_LIBRARY_PATH`로 지정해 돌렸다.
