import 'package:flutter_test/flutter_test.dart';

import 'app_test.dart' show toResult;
import 'fakes.dart';

/// 매초 워치 심박을 보내며 시간을 흘린다.
Future<void> beats(WidgetTester tester, Harness h, int bpm, int seconds) async {
  for (var i = 0; i < seconds; i++) {
    h.watch.beat(bpm);
    await tester.pump(const Duration(seconds: 1));
  }
}

void main() {
  testWidgets('홈에서 워치 연결 → 상태와 심박 표시', (tester) async {
    final h = Harness();
    await h.start(tester);
    await tester.pump(const Duration(milliseconds: 600));
    expect(find.text('워치 연결 안 됨'), findsOneWidget);
    await tapText(tester, '워치 연결하기');
    h.watch.beat(88);
    await tester.pump();
    expect(find.text('워치 연결됨 · 심박 88'), findsOneWidget);
    expect(find.text('워치 연결 끊기'), findsOneWidget);
  });

  testWidgets('같은 심박 126이어도 워치(B 등급)는 중단하지 않고 일시정지까지만', (tester) async {
    final h = Harness();
    await h.start(tester);
    await tester.pump(const Duration(milliseconds: 600));
    await tapText(tester, '워치 연결하기');
    await toResult(tester);
    await tapText(tester, '3분 시작하기');
    await beats(tester, h, 95, 10);
    expect(find.textContaining('디즈먼트 워치 (실시간)'), findsOneWidget);
    expect(find.textContaining('지금 심박 95회/분 · 오늘 상한 109회/분'), findsOneWidget);
    await beats(tester, h, 126, 2);
    expect(find.text('잠깐 쉬는 중'), findsOneWidget);
    expect(find.textContaining('워치는 참고용이라 멈추지 않고'), findsOneWidget);
    expect(find.text('괜찮으세요?'), findsNothing);              // 응급 흐름으로 가지 않음
    // 앉아서 쉬는 동안 심박이 내려옴. 쉬는 중 급하강은 이미 일시정지라 새 행동 없음.
    // (쉬자마자 다시 하기를 누르면 10초 창 안의 126→96 하강이 '급변'으로 또 일시정지된다 — 자문단 확인 항목)
    await beats(tester, h, 96, 12);
    expect(find.text('잠깐 쉬는 중'), findsOneWidget);
    await tapText(tester, '다시 하기');
    await beats(tester, h, 96, 3);
    expect(find.text('남은 시간'), findsOneWidget);
  });

  testWidgets('워치 신호가 15초 넘게 끊기면 채우지 않고 끊김으로 대처', (tester) async {
    final h = Harness();
    await h.start(tester);
    await tester.pump(const Duration(milliseconds: 600));
    await tapText(tester, '워치 연결하기');
    await toResult(tester);
    await tapText(tester, '3분 시작하기');
    await beats(tester, h, 95, 5);
    await seconds(tester, 17);                                    // 심박 없이 시간만
    expect(find.textContaining('워치 신호가 끊겼어요'), findsOneWidget);
    await beats(tester, h, 97, 2);                                 // 다시 들어오면 안내를 거둔다
    expect(find.textContaining('워치 신호가 끊겼어요'), findsNothing);
  });

  testWidgets('워치 없이 시작하면 폰만으로(심박 카드 없음)', (tester) async {
    final h = Harness();
    await h.start(tester);
    await toResult(tester);
    await tapText(tester, '3분 시작하기');
    await tester.pump(const Duration(seconds: 1));
    expect(find.textContaining('디즈먼트 워치'), findsNothing);
  });
}
