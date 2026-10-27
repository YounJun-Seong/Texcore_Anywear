import 'package:flutter_tts/flutter_tts.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';

/// 안내 음성(기본 켜짐). 운동 중에는 화면을 보지 않아도 되게 짧은 문장으로 말한다.
abstract class Speaker {
  Future<void> say(String text);
  Future<void> setRate(double rate);
}

class TtsSpeaker implements Speaker {
  final _tts = FlutterTts();
  TtsSpeaker() {
    _tts.setLanguage('ko-KR');
    _tts.setSpeechRate(0.45);
  }
  @override
  Future<void> say(String text) async {
    await _tts.stop();
    await _tts.speak(text);
  }

  @override
  Future<void> setRate(double rate) => _tts.setSpeechRate(rate);
}

abstract class Dialer {
  Future<void> call(String number);
}

class PhoneDialer implements Dialer {
  @override
  Future<void> call(String number) => launchUrl(Uri(scheme: 'tel', path: number));
}

/// 로그인 토큰·글자 크기 같은 작은 설정만 기기에 둔다. 건강 정보는 기기 설정에 저장하지 않는다.
abstract class LocalStore {
  Future<String?> read(String key);
  Future<void> write(String key, String? value);
}

class PrefsStore implements LocalStore {
  @override
  Future<String?> read(String key) async => (await SharedPreferences.getInstance()).getString(key);
  @override
  Future<void> write(String key, String? value) async {
    final p = await SharedPreferences.getInstance();
    value == null ? await p.remove(key) : await p.setString(key, value);
  }
}
