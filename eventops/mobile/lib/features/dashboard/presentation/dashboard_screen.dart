import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';
import 'package:lucide_icons/lucide_icons.dart';

import '../../../core/router/app_router.dart';
import '../../../shared/widgets/app_scaffold.dart';
import '../presentation/dashboard_cubit.dart';

class DashboardScreen extends StatelessWidget {
  final Widget child;

  const DashboardScreen({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    final cubit = context.read<DashboardCubit>();
    final location = GoRouterState.of(context).uri.toString();

    return AppScaffold(
      title: 'EventOps',
      sidebarItems: [
        SidebarItem(
          icon: LucideIcons.layoutDashboard,
          label: 'Dashboard',
          isActive: location == '/dashboard',
          onTap: () => context.go('/dashboard'),
        ),
        SidebarItem(
          icon: LucideIcons.calendar,
          label: 'Schedule',
          isActive: location == '/schedule',
          onTap: () => context.go('/schedule'),
        ),
        SidebarItem(
          icon: LucideIcons.checkSquare,
          label: 'Tasks',
          isActive: location == '/tasks',
          onTap: () => context.go('/tasks'),
        ),
        SidebarItem(
          icon: LucideIcons.messageSquare,
          label: 'Chat',
          badgeCount: 3,
          isActive: location == '/chat',
          onTap: () => context.go('/chat'),
        ),
        SidebarItem(icon: LucideIcons.fileText, label: 'Documents'),
        SidebarItem(icon: LucideIcons.package, label: 'Inventory'),
        SidebarItem(icon: LucideIcons.users, label: 'Teams'),
        SidebarItem(
          icon: LucideIcons.logOut,
          label: 'Logout',
          onTap: () => context.go('/login'),
        ),
      ],
      body: child,
    );
  }
}
