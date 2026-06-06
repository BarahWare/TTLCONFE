import 'package:flutter_bloc/flutter_bloc.dart';

import '../data/dashboard_repository.dart';

class DashboardState {
  final DashboardMetrics? metrics;
  final bool loading;
  final String? error;

  const DashboardState({this.metrics, this.loading = false, this.error});
}

class DashboardCubit extends Cubit<DashboardState> {
  final DashboardRepository repository;

  DashboardCubit(this.repository) : super(const DashboardState());

  Future<void> load(int eventId) async {
    emit(const DashboardState(loading: true));
    try {
      final metrics = await repository.getMetrics(eventId);
      emit(DashboardState(metrics: metrics));
    } catch (e) {
      emit(DashboardState(error: e.toString()));
    }
  }
}
