// 웹 데모용 다리: 검증된 Dart 안전 엔진을 JS 전역 객체 SafetyEngine으로 내보낸다.
// 빌드: dart compile js -O2 -o ../demo/engine.js web/bridge.dart
// 모든 함수는 JSON 문자열을 받고 JSON 문자열을 돌려준다.
import 'dart:convert';
import 'dart:js_interop';
import 'dart:js_interop_unsafe';

import 'package:safety_engine/safety_engine.dart';

RuleBundle? _rules;
final _monitors = <int, SessionMonitor>{};
final _flows = <int, EmergencyFlow>{};
var _nextId = 1;

RuleBundle get rules => _rules ?? (throw StateError('load() first'));

Profile _profile(Map j) => Profile(
      age: j['age'] as int,
      conditions: {...(j['conditions'] as List? ?? const []).cast<String>()},
      parqRisk: j['parq_risk'] == true,
      doctorClearance: j['doctor_clearance'] == true,
      device: j['device'] as String?,
      betaBlocker: j['beta_blocker'] == true,
      doctorLimits: DoctorLimits.fromJson((j['doctor_limits'] as Map?)?.cast<String, dynamic>()),
    );

List<Map<String, dynamic>> _actions(List<SafetyAction> acts) =>
    [for (final a in acts) {'t': a.t, 'kind': a.kind.name, 'code': a.code, 'detail': a.detail}];

List<List<String?>> _steps(List<EmStep> steps) => [for (final s in steps) [s.$1.name, s.$2]];

String _call(String Function(Map<String, dynamic>) f, String arg) {
  try {
    return jsonEncode({'ok': true, 'result': jsonDecode(f(jsonDecode(arg) as Map<String, dynamic>))});
  } catch (e) {
    return jsonEncode({'ok': false, 'error': '$e'});
  }
}

final _api = <String, String Function(Map<String, dynamic>)>{
  // {bundle: {...규칙 번들 rules 부분}} → 버전 정보
  'load': (j) {
    _rules = RuleBundle.fromMap((j['bundle'] as Map).cast<String, dynamic>());
    return jsonEncode({'version': rules.version, 'status': rules['meta']['status']});
  },
  // {profile, vitals: {systolic, diastolic, resting_hr, bp_source, hr_source}, symptoms, conditions}
  'preCheck': (j) {
    final v = j['vitals'] as Map;
    final d = preCheck(
      rules,
      _profile(j['profile'] as Map),
      Vitals(
        systolic: v['systolic'] as num?,
        diastolic: v['diastolic'] as num?,
        restingHr: v['resting_hr'] as num?,
        bpSource: v['bp_source'] as String? ?? 'manual',
        hrSource: v['hr_source'] as String? ?? 'manual',
      ),
      symptoms: (j['symptoms'] as List? ?? const []).cast<String>(),
      conditions: (j['conditions'] as List? ?? const []).cast<String>(),
    );
    return jsonEncode({'outcome': d.outcome, 'reasons': d.reasons, 'rule_version': d.ruleVersion, 'detail': d.detail});
  },
  'allowance': (j) => jsonEncode(allowance(rules, lightOf(j['light'] as String), j['minutes'] as int)),
  'postCheck': (j) {
    final d = postCheck(rules, j['resting_hr'] as num, j['hr_after_recovery'] as num);
    return jsonEncode({'outcome': d.outcome, 'reasons': d.reasons});
  },
  'hrLimits': (j) {
    final l = hrLimits(rules, _profile(j['profile'] as Map),
        weeksSinceStart: j['weeks'] as int? ?? 0,
        escalationApproved: j['escalation'] == true,
        light: lightOf(j['light'] as String? ?? 'GREEN'));
    return jsonEncode({'max_hr': l.maxHr, 'ceiling_pct': l.ceilingPct, 'ceiling': l.ceiling, 'zone_lower': l.zoneLower, 'mode': l.mode});
  },
  // {ceiling, hr_grade} → {id}
  'monitorNew': (j) {
    final id = _nextId++;
    _monitors[id] = SessionMonitor(rules, j['ceiling'] as int, hrGrade: j['hr_grade'] as String?);
    return jsonEncode({'id': id});
  },
  // {id, event: tick|hr|rpe|symptom|user_stop|interaction|resume, t, value}
  'monitorEvent': (j) {
    final m = _monitors[j['id'] as int]!;
    final t = j['t'] as num;
    final v = j['value'];
    final acts = switch (j['event'] as String) {
      'tick' => m.tick(t),
      'hr' => m.onHr(t, v as num),
      'rpe' => m.onRpe(t, v as Object),
      'symptom' => m.onSymptom(t, v as String),
      'user_stop' => m.onUserStop(t),
      'interaction' => m.onInteraction(t),
      'resume' => m.resume(t),
      final e => throw ArgumentError('unknown event $e'),
    };
    return jsonEncode({'actions': _actions(acts), 'stopped': m.stopped, 'paused': m.paused});
  },
  // {t, severe} → {id, started, state}
  'flowNew': (j) {
    final id = _nextId++;
    final f = _flows[id] = EmergencyFlow(rules, j['t'] as num, severe: j['severe'] == true);
    return jsonEncode({'id': id, 'actions': _steps(f.started), 'state': f.state.name});
  },
  // {id, op: answer|report_severe|confirm_119|tick, t, ok}
  'flowEvent': (j) {
    final f = _flows[j['id'] as int]!;
    final t = j['t'] as num;
    final steps = switch (j['op'] as String) {
      'answer' => f.answer(t, j['ok'] == true),
      'report_severe' => f.reportSevere(t),
      'confirm_119' => f.confirm119(t),
      'tick' => f.tick(t),
      final o => throw ArgumentError('unknown op $o'),
    };
    return jsonEncode({'actions': _steps(steps), 'state': f.state.name});
  },
};

void main() {
  final api = JSObject();
  _api.forEach((name, f) {
    api.setProperty(name.toJS, ((JSString arg) => _call(f, arg.toDart).toJS).toJS);
  });
  globalContext.setProperty('SafetyEngine'.toJS, api);
}
