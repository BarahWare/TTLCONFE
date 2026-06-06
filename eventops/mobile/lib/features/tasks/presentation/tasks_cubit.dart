import 'package:flutter_bloc/flutter_bloc.dart';

import '../data/task_repository.dart';

class TasksState {
  final List<TaskItem> items;
  final bool loading;
  final String? error;
  final String filter;

  const TasksState({
    this.items = const [],
    this.loading = false,
    this.error,
    this.filter = 'All',
  });
}

class TasksCubit extends Cubit<TasksState> {
  final TaskRepository repository;

  TasksCubit(this.repository) : super(const TasksState());

  Future<void> load(int eventId) async {
    emit(const TasksState(loading: true));
    try {
      final items = await repository.getByEvent(eventId);
      emit(TasksState(items: items));
    } catch (e) {
      emit(TasksState(error: e.toString()));
    }
  }

  void setFilter(String filter) {
    final state = this.state;
    emit(TasksState(items: state.items, filter: filter));
  }

  List<TaskItem> get filteredItems {
    final items = state.items;
    if (state.filter == 'All') return items;
    return items.where((t) => t.status == state.filter.toLowerCase()).toList();
  }
}
