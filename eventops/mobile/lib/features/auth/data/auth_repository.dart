import '../../../core/network/api_client.dart';
import '../../../core/storage/local_storage.dart';

class AuthRepository {
  final ApiClient api;

  AuthRepository(this.api);

  Future<String> login(String email, String password) async {
    final response = await api.post('/api/v1/auth/login', data: {
      'email': email,
      'password': password,
    });
    final token = response.data['access_token'] as String;
    LocalStorage.token = token;
    return token;
  }

  void logout() => LocalStorage.token = null;

  bool get isAuthenticated => LocalStorage.token != null;
}
