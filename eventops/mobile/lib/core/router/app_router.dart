import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/presentation/login_screen.dart';
import '../../features/chat/presentation/chat_screen.dart';
import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/schedule/presentation/schedule_screen.dart';
import '../../features/tasks/presentation/tasks_screen.dart';

final GlobalKey<NavigatorState> _rootNavigator = GlobalKey<NavigatorState>(debugLabel: 'root');
final GlobalKey<NavigatorState> _shellNavigator = GlobalKey<NavigatorState>(debugLabel: 'shell');

final GoRouter appRouter = GoRouter(
  navigatorKey: _rootNavigator,
  initialLocation: '/login',
  routes: [
    GoRoute(
      path: '/login',
      builder: (_, __) => const LoginScreen(),
    ),
    ShellRoute(
      navigatorKey: _shellNavigator,
      builder: (_, __, child) => DashboardScreen(child: child),
      routes: [
        GoRoute(
          path: '/dashboard',
          builder: (_, __) => const _PlaceholderBody(),
        ),
        GoRoute(
          path: '/schedule',
          builder: (_, __) => const ScheduleScreen(),
        ),
        GoRoute(
          path: '/tasks',
          builder: (_, __) => const TasksScreen(),
        ),
        GoRoute(
          path: '/chat',
          builder: (_, __) => const ChatScreen(),
        ),
      ],
    ),
  ],
);

class _PlaceholderBody extends StatelessWidget {
  const _PlaceholderBody();

  @override
  Widget build(BuildContext context) {
    return const Center(child: Text('Dashboard', style: TextStyle(color: Colors.white)));
  }
}
