// Python 기준 구현과 같은 정답표(../safety/scenarios)를 단말 엔진으로 재생한다.
// 하나라도 어긋나면 실패: 단말과 서버가 같은 입력에 다른 판정을 내리면 안 된다.
import 'dart:io';

import 'package:safety_engine/safety_engine.dart';
import 'package:test/test.dart';

import 'support.dart';

void main() {
  final rules = loadYamlRules();
  final dir = '${Directory.current.path}/../safety/scenarios';
  var total = 0;

  group('precheck.csv', () {
    for (final row in readCsv('$dir/precheck.csv')) {
      total++;
      test('${row['id']} ${row['note']}', () {
        final profile = Profile(
          age: int.parse(row['age']!),
          conditions: splitSet(row['gate_conditions']),
          parqRisk: row['parq_risk'] == '1',
          doctorClearance: row['clearance'] == '1',
          device: (row['device'] ?? '').isEmpty ? null : row['device'],
          doctorLimits: DoctorLimits(
            systolicMax: numOrNull(row['dr_sbp_max']),
            diastolicMax: numOrNull(row['dr_dbp_max']),
            restingHrMax: numOrNull(row['dr_hr_max']),
            exerciseHrCeiling: numOrNull(row['dr_hr_ceiling']),
          ),
        );
        final d = preCheck(
          rules,
          profile,
          Vitals(
            systolic: numOrNull(row['sbp']),
            diastolic: numOrNull(row['dbp']),
            restingHr: numOrNull(row['hr']),
            bpSource: row['bp_source']!,
            hrSource: row['hr_source']!,
          ),
          symptoms: splitSet(row['symptoms']),
          conditions: splitSet(row['conditions']),
        );
        expect(d.outcome, row['expected']);
        for (final code in splitSet(row['expected_codes'])) {
          expect(d.reasons, contains(code));
        }
      });
    }
  });

  group('hr_limits.csv', () {
    for (final row in readCsv('$dir/hr_limits.csv')) {
      total++;
      test('${row['id']} ${row['note']}', () {
        final p = Profile(
          age: int.parse(row['age']!),
          betaBlocker: row['beta_blocker'] == '1',
          device: (row['device'] ?? '').isEmpty ? null : row['device'],
          doctorLimits: DoctorLimits(exerciseHrCeiling: numOrNull(row['dr_hr_ceiling'])),
        );
        final lim = hrLimits(rules, p,
            weeksSinceStart: int.parse(row['weeks']!),
            escalationApproved: row['escalation'] == '1',
            light: lightOf(row['light']!));
        expect(lim.ceiling, int.parse(row['expected_ceiling']!));
        expect(lim.mode, row['expected_mode']);
      });
    }
  });

  group('post_and_allowance.csv', () {
    for (final row in readCsv('$dir/post_and_allowance.csv')) {
      total++;
      test('${row['id']} ${row['note']}', () {
        if (row['kind'] == 'post_check') {
          expect(postCheck(rules, int.parse(row['a']!), int.parse(row['b']!)).outcome, row['expected']);
        } else {
          expect(allowance(rules, lightOf(row['a']!), int.parse(row['b']!))['max_minutes'], int.parse(row['expected']!));
        }
      });
    }
  });

  group('session.yaml', () {
    for (final sc in readYamlList('$dir/session.yaml')) {
      total++;
      test('${sc['id']} ${sc['desc']}', () {
        final m = SessionMonitor(rules, sc['ceiling'] as int, hrGrade: sc['hr_grade'] as String?);
        final got = <List<Object>>[];
        for (final (t, kind, v) in expandEvents(sc['events'] as List)) {
          final acts = switch (kind) {
            'hr' => m.onHr(t, v as num),
            'tick' => m.tick(t),
            'rpe' => m.onRpe(t, v!),
            'symptom' => m.onSymptom(t, v as String),
            'user_stop' => m.onUserStop(t),
            'interaction' => m.onInteraction(t),
            'resume' => m.resume(t),
            _ => throw StateError(kind),
          };
          got.addAll(acts.map((a) => [a.t, a.kind.name, a.code]));
        }
        final expected = [for (final e in sc['expected'] as List) [e[0] as num, e[1] as String, e[2] as String]];
        expect(got.map((e) => e.join('|')).toList(), expected.map((e) => e.join('|')).toList());
      });
    }
  });

  group('emergency.yaml', () {
    for (final sc in readYamlList('$dir/emergency.yaml')) {
      total++;
      test('${sc['id']} ${sc['desc']}', () {
        List<String> fmt(List<EmStep> steps) => [for (final s in steps) '${s.$1.name}|${s.$2}'];
        List<String> exp(List e) => [for (final x in e) '${x[0]}|${x[1]}'];
        final flow = EmergencyFlow(rules, sc['start']['t'] as num, severe: sc['start']['severe'] as bool);
        expect(fmt(flow.started), exp(sc['start_expected'] as List));
        for (final step in sc['steps'] as List) {
          final t = step[0] as num;
          final acts = switch (step[1] as String) {
            'answer' => flow.answer(t, step[2] as bool),
            'report_severe' => flow.reportSevere(t),
            'confirm_119' => flow.confirm119(t),
            'tick' => flow.tick(t),
            _ => throw StateError('${step[1]}'),
          };
          expect(fmt(acts), exp(step[3] as List), reason: 'step at t=$t');
        }
        expect(flow.state.name, sc['final']);
      });
    }
  });

  test('정답표 300건 이상 (계약 조건)', () => expect(total, greaterThanOrEqualTo(300)));
}
