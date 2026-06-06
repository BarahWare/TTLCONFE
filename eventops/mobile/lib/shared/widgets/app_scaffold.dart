import 'package:flutter/material.dart';

import '../../core/theme/app_colors.dart';
import '../../core/theme/app_spacing.dart';

class AppScaffold extends StatefulWidget {
  final String title;
  final List<SidebarItem> sidebarItems;
  final Widget body;
  final int? trailingBadgeCount;

  const AppScaffold({
    super.key,
    required this.title,
    required this.sidebarItems,
    required this.body,
    this.trailingBadgeCount,
  });

  @override
  State<AppScaffold> createState() => _AppScaffoldState();
}

class _AppScaffoldState extends State<AppScaffold> with SingleTickerProviderStateMixin {
  bool _collapsed = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            curve: Curves.easeOut,
            width: _collapsed ? 64 : 224,
            color: AppColors.background,
            child: Column(
              children: [
                _buildSidebarHeader(),
                const Divider(height: 1, color: AppColors.outline),
                Expanded(child: _buildSidebarItems()),
              ],
            ),
          ),
          const VerticalDivider(width: 1, color: AppColors.outline),
          Expanded(
            child: Column(
              children: [
                _buildTopBar(),
                const Divider(height: 1, color: AppColors.outline),
                Expanded(child: widget.body),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSidebarHeader() {
    return SizedBox(
      height: 52,
      child: Row(
        children: [
          const SizedBox(width: AppSpacing.md),
          if (!_collapsed) ...[
            const Icon(Icons.hexagon_outlined, color: AppColors.primary, size: 20),
            const SizedBox(width: AppSpacing.sm),
            const Text('EventOps', style: TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.w600)),
          ],
          const Spacer(),
          IconButton(
            icon: Icon(_collapsed ? Icons.chevron_right : Icons.chevron_left, size: 16),
            onPressed: () => setState(() => _collapsed = !_collapsed),
            color: AppColors.textSecondary,
          ),
        ],
      ),
    );
  }

  Widget _buildSidebarItems() {
    return ListView(
      padding: EdgeInsets.zero,
      children: widget.sidebarItems.map((item) {
        final isActive = item.isActive ?? false;
        return Container(
          height: 40,
          margin: const EdgeInsets.symmetric(horizontal: AppSpacing.xs, vertical: 2),
          decoration: BoxDecoration(
            color: isActive ? AppColors.primary.withOpacity(0.15) : null,
            borderRadius: BorderRadius.circular(AppRadius.xs),
          ),
          child: InkWell(
            onTap: item.onTap,
            borderRadius: BorderRadius.circular(AppRadius.xs),
            child: Row(
              children: [
                const SizedBox(width: AppSpacing.sm),
                Icon(item.icon, size: 16, color: isActive ? AppColors.primary : AppColors.textSecondary),
                if (!_collapsed) ...[
                  const SizedBox(width: AppSpacing.sm),
                  Text(
                    item.label,
                    style: TextStyle(
                      color: isActive ? AppColors.primary : AppColors.textSecondary,
                      fontSize: 14,
                    ),
                  ),
                  const Spacer(),
                  if (item.badgeCount != null)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: AppColors.primary.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        '${item.badgeCount}',
                        style: const TextStyle(color: AppColors.primary, fontSize: 11, fontWeight: FontWeight.w600),
                      ),
                    ),
                  const SizedBox(width: AppSpacing.sm),
                ],
              ],
            ),
          ),
        );
      }).toList(),
    );
  }

  Widget _buildTopBar() {
    return Container(
      height: 44,
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
      child: Row(
        children: [
          const Spacer(),
          if (widget.trailingBadgeCount != null)
            Stack(
              children: [
                const Icon(Icons.notifications_outlined, color: AppColors.textSecondary, size: 20),
                Positioned(
                  right: 0,
                  top: 0,
                  child: Container(
                    width: 8,
                    height: 8,
                    decoration: const BoxDecoration(
                      color: AppColors.error,
                      shape: BoxShape.circle,
                    ),
                  ),
                ),
              ],
            ),
          const SizedBox(width: AppSpacing.md),
          const CircleAvatar(
            radius: 14,
            backgroundColor: AppColors.primary,
            child: Icon(Icons.person, size: 16, color: Colors.white),
          ),
        ],
      ),
    );
  }
}

class SidebarItem {
  final IconData icon;
  final String label;
  final VoidCallback? onTap;
  final bool? isActive;
  final int? badgeCount;

  const SidebarItem({
    required this.icon,
    required this.label,
    this.onTap,
    this.isActive,
    this.badgeCount,
  });
}
