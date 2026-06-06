import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';

import 'core/network/api_client.dart';
import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/data/auth_repository.dart';
import 'features/auth/presentation/auth_bloc.dart';
import 'features/chat/data/chat_repository.dart';
import 'features/dashboard/data/dashboard_repository.dart';
import 'features/schedule/data/schedule_repository.dart';
import 'features/tasks/data/task_repository.dart';

class EventOpsApp extends StatelessWidget {
  EventOpsApp({super.key});

  final ApiClient _api = ApiClient();

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => AuthCubit(AuthRepository(_api))),
        BlocProvider(create: (_) => DashboardCubit(DashboardRepository(_api))),
        BlocProvider(create: (_) => ScheduleCubit(ScheduleRepository(_api))),
        BlocProvider(create: (_) => TasksCubit(TaskRepository(_api))),
        BlocProvider(create: (_) => ChatCubit(ChatRepository(_api))),
      ],
      child: MaterialApp.router(
        title: 'EventOps',
        theme: darkTheme,
        routerConfig: appRouter,
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
