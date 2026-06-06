import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lucide_icons/lucide_icons.dart';

import '../../../shared/widgets/app_scaffold.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'EventOps',
      sidebarItems: [
        SidebarItem(icon: LucideIcons.layoutDashboard, label: 'Dashboard', isActive: true),
        SidebarItem(icon: LucideIcons.calendar, label: 'Schedule'),
        SidebarItem(icon: LucideIcons.checkSquare, label: 'Tasks'),
        SidebarItem(icon: LucideIcons.messageSquare, label: 'Chat', badgeCount: 3),
        SidebarItem(icon: LucideIcons.fileText, label: 'Documents'),
        SidebarItem(icon: LucideIcons.package, label: 'Inventory'),
        SidebarItem(icon: LucideIcons.users, label: 'Teams'),
        SidebarItem(icon: LucideIcons.logOut, label: 'Logout', onTap: () => context.go('/login')),
      ],
      body: const Center(
        child: Text('Dashboard', style: TextStyle(color: Colors.white)),
      ),
    );
  }
}
