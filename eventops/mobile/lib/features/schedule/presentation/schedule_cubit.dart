import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../data/schedule_repository.dart';

class ScheduleState {
  final List<ScheduleItem> items;
  final bool loading;
  final String? error;

  const ScheduleState({
    this.items = const [],
    this.loading = false,
    this.error,
  });
}

class ScheduleCubit extends Cubit<ScheduleState> {
  final ScheduleRepository repository;

  ScheduleCubit(this.repository) : super(const ScheduleState());

  Future<void> load(int eventId) async {
    emit(const ScheduleState(loading: true));
    try {
      final items = await repository.getByEvent(eventId);
      emit(ScheduleState(items: items));
    } catch (e) {
      emit(ScheduleState(error: e.toString()));
    }
  }
}
