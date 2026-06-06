import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../shared/widgets/app_card.dart';
import '../data/task_repository.dart';
import '../presentation/tasks_cubit.dart';

class TasksScreen extends StatefulWidget {
  const TasksScreen({super.key});

  @override
  State<TasksScreen> createState() => _TasksScreenState();
}

class _TasksScreenState extends State<TasksScreen> {
  final _filters = ['All', 'Pending', 'Done'];

  @override
  void initState() {
    super.initState();
    context.read<TasksCubit>().load(1);
  }

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<TasksCubit, TasksState>(
      builder: (context, state) {
        return Padding(
          padding: const EdgeInsets.all(AppSpacing.md),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Tasks',
                  style: TextStyle(
                      color: AppColors.textPrimary,
                      fontSize: 24,
                      fontWeight: FontWeight.w600)),
              const SizedBox(height: AppSpacing.md),
              Row(
                children: _filters
                    .map((f) => Padding(
                          padding: const EdgeInsets.only(right: AppSpacing.sm),
                          child: ChoiceChip(
                            label: Text(f),
                            selected: state.filter == f,
                            onSelected: (_) =>
                                context.read<TasksCubit>().setFilter(f),
                            selectedColor: AppColors.primary.withOpacity(0.2),
                            labelStyle: TextStyle(
                              color: state.filter == f
                                  ? AppColors.primary
                                  : AppColors.textSecondary,
                            ),
                          ),
                        ))
                    .toList(),
              ),
              const SizedBox(height: AppSpacing.md),
              Expanded(
                child: ListView.builder(
                  itemCount: context.read<TasksCubit>().filteredItems.length,
                  itemBuilder: (_, i) {
                    final task = context.read<TasksCubit>().filteredItems[i];
                    return Padding(
                      padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                      child: AppCard(
                        child: ListTile(
                          leading: Icon(
                            task.status == 'completed'
                                ? Icons.check_circle
                                : Icons.radio_button_unchecked,
                            color: task.status == 'completed'
                                ? AppColors.success
                                : AppColors.textSecondary,
                          ),
                          title: Text(task.title,
                              style: const TextStyle(
                                  color: AppColors.textPrimary)),
                          subtitle: task.priority != null
                              ? Text(task.priority!,
                                  style: TextStyle(
                                    color: task.priority == 'high'
                                        ? AppColors.warning
                                        : AppColors.textSecondary,
                                    fontSize: 12,
                                  ))
                              : null,
                        ),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
