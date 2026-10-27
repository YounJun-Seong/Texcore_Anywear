// 실제 watch_bridge.py(가상 워치)와 연결 시험. 브리지가 없으면 건너뜀.
//   python ../watch_bridge/watch_bridge.py serve --simulate --interval 0.2 &
//   WATCH_BRIDGE=ws://127.0.0.1:8765 flutter test test/bridge_contract_test.dart
@TestOn('vm')
library;

import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:senior_coach/core/heart_rate.dart';

void main() {
  final url = Platform.environment['WATCH_BRIDGE'];
  test('PC 브리지에서 심박과 상태를 받는다', () async {
    final src = BridgeHeartRateSource(url!);
    final statuses = <String>[];
    src.status.listen(statuses.add);
    final first = src.samples.take(3).toList();
    await src.connect();
    expect(src.connected, isTrue);
    final got = await first.timeout(const Duration(seconds: 10));
    expect(got.map((s) => s.bpm), everyElement(inInclusiveRange(60, 160)));
    expect(statuses, contains('워치 연결됨'));
    await src.close();
    expect(src.connected, isFalse);
  }, skip: url == null ? 'WATCH_BRIDGE 없으면 건너뜀' : null);

  test('브리지가 없으면 안내 문장을 낸다', () async {
    final src = BridgeHeartRateSource('ws://127.0.0.1:1');
    final statuses = <String>[];
    src.status.listen(statuses.add);
    await expectLater(src.connect(), throwsA(anything));
    await Future<void>.delayed(Duration.zero);
    expect(statuses.last, contains('watch_bridge.py serve'));
    expect(src.connected, isFalse);
  });
}
