/// 어르신 운동 안전 엔진 — 단말(오프라인) 구현.
///
/// 판정 수치는 서버가 내려주는 승인된 규칙 번들에서만 온다. 운동 중 네트워크가 끊겨도
/// 중단·응급 흐름이 단말 안에서 동작해야 하므로 이 패키지는 외부 호출이 없다.
library;

export 'src/codes.dart';
export 'src/emergency.dart';
export 'src/precheck.dart';
export 'src/rules.dart';
export 'src/session.dart';
