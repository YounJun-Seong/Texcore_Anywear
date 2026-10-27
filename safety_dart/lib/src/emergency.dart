import 'codes.dart';
import 'rules.dart';

/// 응급 흐름(5-4) 상태 기계. Python emergency.py와 같은 전이.
enum EmState { ASK_OK, RESTING_OK, GUARDIAN_ALERTED, SHOW_119, CALLING_119, GUARDIAN_119 }

enum EmAction { REST_GUIDANCE, ASK_OK, SHOW_119, DIAL_119, NOTIFY_GUARDIAN, GUARDIAN_CALL_119 }

typedef EmStep = (EmAction, String?);

const _terminal = {EmState.RESTING_OK, EmState.GUARDIAN_ALERTED, EmState.CALLING_119, EmState.GUARDIAN_119};

class EmergencyFlow {
  final Map e;
  final Map<String, dynamic> snapshot;
  num _now;
  late EmState state;
  late num deadline;
  late final List<EmStep> started;

  EmergencyFlow(RuleBundle r, num t, {required bool severe, this.snapshot = const {}})
      : e = r['emergency'],
        _now = t {
    started = severe ? _show119(t, Code.emSevereSymptom) : _askOk(t);
  }

  bool get finished => _terminal.contains(state);

  List<EmStep> _askOk(num t) {
    state = EmState.ASK_OK;
    deadline = t + e['ask_ok_timeout_seconds'];
    return const [(EmAction.REST_GUIDANCE, null), (EmAction.ASK_OK, null)];
  }

  List<EmStep> _show119(num t, String code) {
    state = EmState.SHOW_119;
    deadline = t + e['call_119_confirm_timeout_seconds'];
    return [(EmAction.SHOW_119, code)];
  }

  bool _advance(num t) {
    if (t < _now) throw ArgumentError('time went backwards');
    _now = t;
    return !finished;
  }

  List<EmStep> answer(num t, bool ok) {
    if (!_advance(t) || state != EmState.ASK_OK) return const [];
    if (ok) {
      state = EmState.RESTING_OK;
      return const [(EmAction.REST_GUIDANCE, Code.emUserOk)];
    }
    state = EmState.GUARDIAN_ALERTED;
    return const [(EmAction.NOTIFY_GUARDIAN, Code.emUserNotOk)];
  }

  /// "괜찮으세요?" 단계에서 흉통·실신감·마비 등이 새로 보고됨 → 119로 올린다.
  List<EmStep> reportSevere(num t) {
    if (!_advance(t) || state != EmState.ASK_OK) return const [];
    return _show119(t, Code.emSevereSymptom);
  }

  List<EmStep> confirm119(num t) {
    if (!_advance(t) || state != EmState.SHOW_119) return const [];
    state = EmState.CALLING_119;
    return const [(EmAction.DIAL_119, Code.em119Confirmed), (EmAction.NOTIFY_GUARDIAN, Code.em119Confirmed)];
  }

  List<EmStep> tick(num t) {
    if (!_advance(t) || t < deadline) return const [];
    if (state == EmState.ASK_OK) {
      state = EmState.GUARDIAN_ALERTED;
      return const [(EmAction.NOTIFY_GUARDIAN, Code.emNoResponse)];
    }
    if (state == EmState.SHOW_119) {
      state = EmState.GUARDIAN_119;
      return const [(EmAction.GUARDIAN_CALL_119, Code.em119NoConfirm)];
    }
    return const [];
  }
}
