import 'package:flutter_bloc/flutter_bloc.dart';

enum AuthStatus { initial, loading, authenticated, unauthenticated, error }

class AuthState {
  final AuthStatus status;
  final String? error;
  final String? token;

  const AuthState({this.status = AuthStatus.initial, this.error, this.token});
}

class AuthCubit extends Cubit<AuthState> {
  AuthCubit() : super(const AuthState());

  Future<void> login(String email, String password) async {
    emit(const AuthState(status: AuthStatus.loading));
    try {
      // TODO: call API client
      // final response = await ApiClient().post('/api/v1/auth/login', data: {...});
      // final token = response.data['access_token'];
      emit(AuthState(status: AuthStatus.authenticated, token: 'mock-token'));
    } catch (e) {
      emit(AuthState(status: AuthStatus.error, error: e.toString()));
    }
  }

  void logout() {
    emit(const AuthState(status: AuthStatus.unauthenticated));
  }
}
