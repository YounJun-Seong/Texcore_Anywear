import 'dart:io';

import 'package:safety_engine/safety_engine.dart';
import 'package:yaml/yaml.dart';

final safetyDir = '${Directory.current.path}/../safety';

/// YAML 값을 jsonDecode 결과와 같은 평범한 Map/List로 바꾼다.
dynamic plain(dynamic v) {
  if (v is YamlMap) return {for (final e in v.entries) e.key.toString(): plain(e.value)};
  if (v is YamlList) return [for (final x in v) plain(x)];
  return v;
}

RuleBundle loadYamlRules() =>
    RuleBundle.fromMap(plain(loadYaml(File('$safetyDir/rules/safety_rules.yaml').readAsStringSync())) as Map<String, dynamic>);

List<Map<String, dynamic>> readYamlList(String path) =>
    [for (final x in plain(loadYaml(File(path).readAsStringSync())) as List) x as Map<String, dynamic>];

/// 따옴표가 있는 칸("130/80, 심박 70")을 처리하는 최소 CSV 파서.
List<Map<String, String>> readCsv(String path) {
  var text = File(path).readAsStringSync();
  if (text.startsWith('﻿')) text = text.substring(1);
  final rows = <List<String>>[];
  var row = <String>[], field = StringBuffer();
  var quoted = false;
  for (var i = 0; i < text.length; i++) {
    final ch = text[i];
    if (quoted) {
      if (ch == '"' && i + 1 < text.length && text[i + 1] == '"') {
        field.write('"');
        i++;
      } else if (ch == '"') {
        quoted = false;
      } else {
        field.write(ch);
      }
    } else if (ch == '"') {
      quoted = true;
    } else if (ch == ',') {
      row.add(field.toString());
      field = StringBuffer();
    } else if (ch == '\n' || ch == '\r') {
      if (ch == '\r' && i + 1 < text.length && text[i + 1] == '\n') i++;
      row.add(field.toString());
      field = StringBuffer();
      if (row.any((c) => c.isNotEmpty)) rows.add(row);
      row = <String>[];
    } else {
      field.write(ch);
    }
  }
  if (field.isNotEmpty || row.isNotEmpty) {
    row.add(field.toString());
    rows.add(row);
  }
  final header = rows.first;
  return [for (final r in rows.skip(1)) {for (var i = 0; i < header.length; i++) header[i]: i < r.length ? r[i] : ''}];
}

num? numOrNull(String? v) {
  if (v == null || v.isEmpty) return null;
  final d = double.parse(v);
  return d == d.truncateToDouble() ? d.toInt() : d;
}

Set<String> splitSet(String? v) => {for (final x in (v ?? '').split('|')) if (x.isNotEmpty) x};

/// session.yaml 이벤트 펼치기: 스트림은 매초 1건, 같은 시각은 적힌 순서대로.
List<(num, String, Object?)> expandEvents(List events) {
  final out = <(num, int, String, Object?)>[];
  for (var i = 0; i < events.length; i++) {
    final e = events[i] as Map;
    if (e.containsKey('from')) {
      final kind = e.containsKey('hr') ? 'hr' : 'tick';
      for (var t = e['from'] as int; t <= (e['to'] as int); t++) {
        out.add((t, i, kind, e['hr']));
      }
    } else {
      final kind = ['rpe', 'symptom', 'user_stop', 'interaction', 'resume'].firstWhere(e.containsKey);
      out.add((e['t'] as num, i, kind, e[kind]));
    }
  }
  out.sort((a, b) => a.$1 != b.$1 ? a.$1.compareTo(b.$1) : a.$2.compareTo(b.$2));
  return [for (final x in out) (x.$1, x.$3, x.$4)];
}
