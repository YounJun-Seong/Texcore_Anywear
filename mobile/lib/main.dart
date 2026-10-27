import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';

import 'core/api.dart';
import 'core/app_state.dart';
import 'core/heart_rate.dart';
import 'core/services.dart';
import 'screens/daily.dart';
import 'screens/onboarding.dart';
import 'ui/kit.dart';

// 빌드 시 지정: flutter run --dart-define=API_BASE_URL=https://... --dart-define=ALLOW_DRAFT_RULES=true
const apiBaseUrl = String.fromEnvironment('API_BASE_URL', defaultValue: 'http://10.0.2.2:8000');
const allowDraftRules = bool.fromEnvironment('ALLOW_DRAFT_RULES');
// PC의 watch_bridge.py. 에뮬레이터에서 PC는 10.0.2.2
const watchBridgeUrl = String.fromEnvironment('WATCH_BRIDGE_URL', defaultValue: 'ws://10.0.2.2:8765');

// 시연 녹화용: 접근성 트리를 켜서 자동화 스크립트가 버튼을 글자로 찾게 한다.
const demoSemantics = bool.fromEnvironment('DEMO_SEMANTICS');

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  if (demoSemantics) SemanticsBinding.instance.ensureSemantics();
  final state = AppState(
    api: ApiClient(apiBaseUrl),
    speaker: TtsSpeaker(),
    dialer: PhoneDialer(),
    store: PrefsStore(),
    allowDraftRules: allowDraftRules,
    watch: BridgeHeartRateSource(watchBridgeUrl),
  );
  await state.restore();
  if (state.loggedIn) {
    try {
      await state.loadMe();
    } catch (_) {
      await state.logout();
    }
    state.refreshRules();
  }
  runApp(SeniorCoachApp(state: state));
}

class SeniorCoachApp extends StatelessWidget {
  final AppState state;
  const SeniorCoachApp({super.key, required this.state});

  @override
  Widget build(BuildContext context) => AppScope(
        state: state,
        child: ListenableBuilder(
          listenable: state,
          builder: (context, _) => MaterialApp(
            title: '운동친구',
            debugShowCheckedModeBanner: false,
            theme: seniorTheme(Brightness.light),
            darkTheme: seniorTheme(Brightness.dark),
            themeMode: ThemeMode.system,
            // 글자 크기 3단계(앱 설정) × 기기 글자 크기 설정
            builder: (context, child) => MediaQuery(
              data: MediaQuery.of(context).copyWith(
                textScaler: TextScaler.linear(MediaQuery.textScalerOf(context).scale(1) * state.textScale),
              ),
              child: child!,
            ),
            home: state.loggedIn ? const HomeScreen() : const LoginScreen(),
          ),
        ),
      );
}
