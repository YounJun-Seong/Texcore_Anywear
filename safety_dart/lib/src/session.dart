import 'dart:collection';
import 'dart:math' as math;

import 'codes.dart';
import 'precheck.dart';
import 'rules.dart';

num _round6(num x) => (x * 1e6).round() / 1e6;
int _floor(num x) => _round6(x).floor();

class HrLimits {
  final double maxHr;
  final double ceilingPct;
  final int ceiling;
  final int? zoneLower;
  final String mode; // zone | anomaly_only
  const HrLimits(this.maxHr, this.ceilingPct, this.ceiling, this.zoneLower, this.mode);

  factory HrLimits.fromJson(Map<String, dynamic> j) => HrLimits((j['max_hr'] as num).toDouble(),
      (j['ceiling_pct'] as num).toDouble(), j['ceiling'] as int, j['zone_lower'] as int?, j['mode'] as String);
}

/// 오늘 세션의 심박 상한·목표 구간.
HrLimits hrLimits(RuleBundle r, Profile p, {int weeksSinceStart = 0, bool escalationApproved = false, Light light = Light.GREEN}) {
  final s = r['session'];
  final cp = s['ceiling_pct'];
  final maxHr = (s['max_hr']['intercept'] as num) - (s['max_hr']['age_coef'] as num) * p.age;
  num pct;
  String mode;
  if (p.betaBlocker) {
    pct = cp['absolute_max'];
    mode = 'anomaly_only';
  } else if (weeksSinceStart >= s['initial_period_weeks'] && escalationApproved) {
    pct = cp['escalated'];
    mode = 'zone';
  } else {
    pct = cp['initial'];
    mode = 'zone';
  }
  pct = math.min(pct, cp['absolute_max'] as num);
  final cap = (r['allowance'] as Map)[light.name]?['hr_ceiling_pct_cap'];
  if (cap != null) pct = math.min(pct, cap as num);

  var ceiling = _floor(maxHr * pct);
  final doctor = p.doctorLimits.exerciseHrCeiling;
  if (doctor != null) {
    ceiling = math.min(ceiling, doctor.toInt());
  } else if ((r['hard_gate']['devices_requiring_doctor_hr_ceiling'] as List).contains(p.device)) {
    throw ArgumentError('pacemaker/ICD user without doctor HR ceiling must be blocked by the hard gate');
  }
  final zoneLower = mode == 'anomaly_only' ? null : math.min(_round6(maxHr * s['zone_pct']['lower']).ceil(), ceiling);
  return HrLimits((maxHr * 10).round() / 10, pct.toDouble(), ceiling, zoneLower, mode);
}

class SafetyAction {
  final num t;
  final ActionKind kind;
  final String code;
  final Map<String, dynamic> detail;
  const SafetyAction(this.t, this.kind, this.code, [this.detail = const {}]);

  @override
  String toString() => '[$t, ${kind.name}, $code]';
}

/// 운동 중 규칙(5-3). 1초 간격 tick과 센서·사용자 이벤트를 받아 행동을 돌려준다.
/// 시간은 호출자가 넘기는 초 단위 값만 쓴다(시나리오 재생이 결정론적).
class SessionMonitor {
  final Map s;
  final int ceiling;
  late final bool usesHr;
  ActionKind? _hrMaxAction;
  late final int _normalInterval;
  late int _checkinInterval;
  final void Function(Map<String, dynamic>)? sink;

  num _now;
  bool stopped = false, paused = false, sensorFallback = false;
  num? _overSince, _slowedAt;
  num _lastValidHrT, _lastCheckinT, _lastInteractionT;
  bool _noResponseAlerted = false;
  final _recent = Queue<(num, num)>();

  SessionMonitor(RuleBundle r, this.ceiling, {String? hrGrade, num startT = 0, this.sink})
      : s = r['session'],
        _now = startT,
        _lastValidHrT = startT,
        _lastCheckinT = startT,
        _lastInteractionT = startT {
    final gradeRule = hrGrade == null ? null : s['heart_rate_grades'][hrGrade];
    usesHr = gradeRule != null && gradeRule['use_hr'] == true;
    _hrMaxAction = usesHr ? ActionKind.values.byName(gradeRule['max_hr_action']) : null;
    _normalInterval = usesHr ? s['checkin_interval_seconds'] : s['no_sensor_checkin_interval_seconds'];
    _checkinInterval = _normalInterval;
  }

  // ---- 공개 이벤트 ----
  List<SafetyAction> tick(num t) => _run(t, 'tick', null, (_) {});

  List<SafetyAction> onHr(num t, num bpm) => _run(t, 'hr', bpm, (out) => _hr(t, bpm, out), checkGapFirst: true);

  List<SafetyAction> onRpe(num t, Object answer) {
    final value = _rpeValue(answer);
    return _run(t, 'rpe', answer, (out) {
      _lastCheckinT = t;
      if (value >= s['rpe']['stop_at']) {
        _stop(t, ActionKind.STOP, Code.rpeVeryHard, out, {'rpe': value});
      } else if (value >= s['rpe']['step_down_at']) {
        out.add(SafetyAction(t, ActionKind.STEP_DOWN, Code.rpeHard, {'rpe': value}));
      }
    }, interaction: true);
  }

  List<SafetyAction> onSymptom(num t, String symptom) {
    final ActionKind kind;
    final String code;
    if ((s['emergency_symptoms'] as List).contains(symptom)) {
      kind = ActionKind.EMERGENCY_119;
      code = Code.emergencySymptom;
    } else if ((s['stop_symptoms'] as List).contains(symptom)) {
      kind = ActionKind.STOP;
      code = Code.stopSymptom;
    } else {
      throw ArgumentError('unknown symptom: $symptom');
    }
    return _run(t, 'symptom', symptom, (out) => _stop(t, kind, code, out, {'symptom': symptom}), interaction: true);
  }

  /// 항상 보이는 "그만" 버튼.
  List<SafetyAction> onUserStop(num t) =>
      _run(t, 'user_stop', null, (out) => _stop(t, ActionKind.STOP, Code.userStop, out), interaction: true);

  List<SafetyAction> onInteraction(num t) => _run(t, 'interaction', null, (_) {}, interaction: true);

  List<SafetyAction> resume(num t) => _run(t, 'resume', null, (_) {
        paused = false;
        _overSince = null;
        _slowedAt = null;
        _lastCheckinT = t;
      }, interaction: true);

  // ---- 내부 ----
  List<SafetyAction> _run(num t, String event, Object? value, void Function(List<SafetyAction>) handler,
      {bool interaction = false, bool checkGapFirst = false}) {
    if (t < _now) throw ArgumentError('time went backwards: $t < $_now');
    _now = t;
    if (stopped) return const [];
    final out = <SafetyAction>[];
    if (interaction) {
      _lastInteractionT = t;
      _noResponseAlerted = false;
    }
    if (checkGapFirst) _checkGap(t, out);
    handler(out);
    if (!stopped) _timeChecks(t, out);
    if (out.isNotEmpty && sink != null) {
      sink!({
        't': t,
        'event': event,
        'value': value,
        'actions': [for (final a in out) {'kind': a.kind.name, 'code': a.code, 'detail': a.detail}],
      });
    }
    return out;
  }

  num _rpeValue(Object answer) {
    final r = s['rpe'];
    final num value = answer is String ? r['answer_map'][answer] : answer as num;
    if (!(r['valid']['min'] <= value && value <= r['valid']['max'])) throw ArgumentError('RPE out of range: $answer');
    return value;
  }

  void _stop(num t, ActionKind kind, String code, List<SafetyAction> out, [Map<String, dynamic> detail = const {}]) {
    stopped = true;
    out.add(SafetyAction(t, kind, code, detail));
  }

  /// 심박 기반 중단 신호. B 등급 센서는 일시정지까지만 올린다.
  void _hrAlarm(num t, String code, List<SafetyAction> out, Map<String, dynamic> detail) {
    if (_hrMaxAction == ActionKind.STOP) {
      _stop(t, ActionKind.STOP, code, out, detail);
    } else if (!paused) {
      paused = true;
      out.add(SafetyAction(t, ActionKind.PAUSE, code, detail));
    }
  }

  void _enterFallback(num t, String code, List<SafetyAction> out) {
    if (sensorFallback) return;
    sensorFallback = true;
    _checkinInterval = s['sensor']['fallback_checkin_interval_seconds'];
    _overSince = null;
    _slowedAt = null;
    out.add(SafetyAction(t, ActionKind.SENSOR_FALLBACK, code));
    out.add(SafetyAction(t, ActionKind.STEP_DOWN, code));
  }

  void _checkGap(num t, List<SafetyAction> out) {
    if (usesHr && !sensorFallback && t - _lastValidHrT > s['sensor']['hr_gap_seconds']) {
      _enterFallback(t, Code.sensorGap, out);
    }
  }

  void _hr(num t, num bpm, List<SafetyAction> out) {
    if (!usesHr) return;
    final p = s['sensor']['plausible'];
    if (!(p['min'] <= bpm && bpm <= p['max'])) {
      _enterFallback(t, Code.sensorImplausible, out);
      return;
    }
    _lastValidHrT = t;
    if (sensorFallback) {
      sensorFallback = false;
      _checkinInterval = _normalInterval;
      out.add(SafetyAction(t, ActionKind.SENSOR_RESTORED, Code.sensorOk));
    }
    final sc = s['sudden_change'];
    while (_recent.isNotEmpty && t - _recent.first.$1 > sc['window_seconds']) {
      _recent.removeFirst();
    }
    final jump = _recent.fold<num>(0, (m, e) => math.max(m, (bpm - e.$2).abs()));
    _recent.add((t, bpm));

    if (bpm >= _round6(ceiling * s['stop_ratio_over_ceiling'])) {
      _hrAlarm(t, Code.hrFarOverCeiling, out, {'bpm': bpm, 'ceiling': ceiling});
    } else if (jump >= sc['delta_bpm']) {
      _hrAlarm(t, Code.hrSuddenChange, out, {'bpm': bpm, 'jump': jump});
    }
    if (stopped) return;
    if (bpm > ceiling) {
      _overSince ??= t;
    } else {
      _overSince = null;
      _slowedAt = null;
    }
  }

  void _timeChecks(num t, List<SafetyAction> out) {
    _checkGap(t, out);
    if (!paused && _overSince != null) {
      if (_slowedAt == null && t - _overSince! > s['over_ceiling_seconds_to_slow_down']) {
        _slowedAt = t;
        out.add(SafetyAction(t, ActionKind.SLOW_DOWN, Code.hrOverCeiling, {'ceiling': ceiling}));
      } else if (_slowedAt != null && t - _slowedAt! >= s['recover_seconds_after_slow_down']) {
        paused = true;
        out.add(SafetyAction(t, ActionKind.PAUSE, Code.hrNotRecovered, {'ceiling': ceiling}));
      }
    }
    if (!paused && t - _lastCheckinT >= _checkinInterval) {
      _lastCheckinT = t;
      out.add(SafetyAction(t, ActionKind.ASK_RPE, Code.checkinDue));
    }
    if (!_noResponseAlerted && t - _lastInteractionT >= s['no_response_seconds']) {
      _noResponseAlerted = true;
      out.add(SafetyAction(t, ActionKind.GUARDIAN_ALERT, Code.noResponse));
      out.add(SafetyAction(t, ActionKind.LOUD_PROMPT, Code.noResponse));
    }
  }
}
