import 'package:flutter_bloc/flutter_bloc.dart';

import '../data/auth_repository.dart';

enum AuthStatus { initial, loading, authenticated, unauthenticated, error }

class AuthState {
  final AuthStatus status;
  final String? error;
  final String? token;

  const AuthState({this.status = AuthStatus.initial, this.error, this.token});
}

class AuthCubit extends Cubit<AuthState> {
  final AuthRepository repository;

  AuthCubit(this.repository) : super(const AuthState());

  Future<void> login(String email, String password) async {
    emit(const AuthState(status: AuthStatus.loading));
    try {
      final token = await repository.login(email, password);
      emit(AuthState(status: AuthStatus.authenticated, token: token));
    } catch (e) {
      emit(AuthState(status: AuthStatus.error, error: e.toString()));
    }
  }

  void logout() {
    repository.logout();
    emit(const AuthState(status: AuthStatus.unauthenticated));
  }
}
