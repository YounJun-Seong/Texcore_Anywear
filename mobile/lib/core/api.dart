import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiException implements Exception {
  final int status;
  final String message;
  ApiException(this.status, this.message);
  @override
  String toString() => message;
}

/// 서버(FastAPI) 호출. 모든 화면 문구는 서버 detail을 그대로 보여 줄 수 있게 한국어로 온다.
class ApiClient {
  final String baseUrl;
  final http.Client _http;
  String? token;

  ApiClient(this.baseUrl, {http.Client? client, this.token}) : _http = client ?? http.Client();

  Map<String, String> get _headers => {
        'content-type': 'application/json',
        if (token != null) 'authorization': 'Bearer $token',
      };

  Future<dynamic> _send(String method, String path, [Object? body]) async {
    final uri = Uri.parse('$baseUrl$path');
    final req = http.Request(method, uri)..headers.addAll(_headers);
    if (body != null) req.body = jsonEncode(body);
    final res = await http.Response.fromStream(await _http.send(req));
    final text = utf8.decode(res.bodyBytes);
    if (res.statusCode >= 400) {
      var msg = '잠시 후 다시 해 주세요';
      try {
        final d = jsonDecode(text)['detail'];
        if (d is String) msg = d;
      } catch (_) {}
      throw ApiException(res.statusCode, msg);
    }
    return text.isEmpty ? null : jsonDecode(text);
  }

  Future<dynamic> get(String path) => _send('GET', path);
  Future<dynamic> post(String path, [Object? body]) => _send('POST', path, body ?? {});
  Future<dynamic> put(String path, Object body) => _send('PUT', path, body);

  // ---- 인증 ----
  Future<void> requestOtp(String phone) => post('/auth/otp/request', {'phone': phone});

  /// 처음 가입이면 422(이름·태어난 해 필요)가 온다. 같은 인증번호로 정보를 채워 다시 부른다.
  Future<String> verifyOtp(String phone, String code, {String? name, int? birthYear}) async {
    final r = await post('/auth/otp/verify', {
      'phone': phone,
      'code': code,
      if (name != null) ...{'role': 'elder', 'name': name, 'birth_year': birthYear},
    });
    token = r['token'] as String;
    return token!;
  }

  // ---- 본인 ----
  Future<Map<String, dynamic>> me() async => await get('/me') as Map<String, dynamic>;
  Future<void> consent(String kind, bool granted) => post('/me/consents', {'kind': kind, 'granted': granted});
  Future<void> putHealth(Map<String, dynamic> h) => put('/me/health', h);
  Future<void> putSettings(Map<String, dynamic> s) => put('/me/settings', s);
  Future<List> guardians() async => await get('/me/guardians') as List;
  Future<void> updateGuardian(int linkId, {String? status, String? scope}) =>
      put('/me/guardians/$linkId', {'status': ?status, 'scope': ?scope});

  // ---- 하루 ----
  Future<Map<String, dynamic>> today() async => await get('/me/today') as Map<String, dynamic>;
  Future<Map<String, dynamic>> precheck(Map<String, dynamic> body) async =>
      await post('/me/prechecks', body) as Map<String, dynamic>;
  Future<Map<String, dynamic>> startSession(int precheckId, {bool easier = false}) async =>
      await post('/me/sessions', {'precheck_id': precheckId, 'easier': easier}) as Map<String, dynamic>;
  Future<void> sessionEvents(int sessionId, List<Map<String, dynamic>> events) =>
      post('/me/sessions/$sessionId/events', {'events': events});
  Future<Map<String, dynamic>> finish(int sessionId, Map<String, dynamic> body) async =>
      await post('/me/sessions/$sessionId/finish', body) as Map<String, dynamic>;
  Future<void> emergency(Map<String, dynamic> body) => post('/me/emergency', body);
  Future<Map<String, dynamic>> week() async => await get('/me/week') as Map<String, dynamic>;

  /// 안전 규칙 번들 원문(해시 검증은 RuleBundle.fromEnvelope가 한다).
  Future<String> rulesBundle() async {
    final res = await _http.get(Uri.parse('$baseUrl/rules/safety'));
    if (res.statusCode != 200) throw ApiException(res.statusCode, '안전 규칙을 받지 못했어요');
    return utf8.decode(res.bodyBytes);
  }
}
