# 안전 엔진 — 단말(Dart)

어르신 휴대폰 안에서 오프라인으로 도는 안전 엔진. 운동 중 네트워크가 끊겨도 중단·응급 흐름이 동작해야 하므로(7장) 외부 호출이 없다.
Python 기준 구현(`../safety`)을 그대로 옮겼고, **같은 규칙 번들과 같은 정답표**(`../safety/scenarios`, 352건)를 통과해야 한다.

- `RuleBundle.fromEnvelope(서버 응답)`: 서버 `/rules/safety` 응답을 받아 구조를 검사하고, 해시를 다시 계산해 서버 해시와 맞지 않으면 거부. 운영 빌드는 자문단 승인(approved) 번들만 받는다.
- `preCheck`, `hardGate`, `allowance`, `postCheck`, `hrLimits`, `SessionMonitor`, `EmergencyFlow`: Python과 같은 이름·같은 사유 코드.

```bash
dart pub get && dart test     # 정답표 352건 + 번들 해시·검증 테스트
```
규칙 YAML이 바뀌면 `test/fixtures/bundle_draft.json`을 다시 만든다:
`cd ../safety && python tools/export_bundle.py --allow-draft --out ../safety_dart/test/fixtures/bundle_draft.json`
