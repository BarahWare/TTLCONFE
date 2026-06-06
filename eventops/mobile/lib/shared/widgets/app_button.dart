import 'package:flutter/material.dart';

import '../../core/theme/app_colors.dart';
import '../../core/theme/app_spacing.dart';

enum AppButtonVariant { primary, subtle, ghost, destructive }
enum AppButtonSize { sm, md }

class AppButton extends StatelessWidget {
  final String label;
  final AppButtonVariant variant;
  final AppButtonSize size;
  final VoidCallback? onPressed;
  final bool isLoading;

  const AppButton({
    super.key,
    required this.label,
    this.variant = AppButtonVariant.primary,
    this.size = AppButtonSize.md,
    this.onPressed,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: size == AppButtonSize.md ? 40 : 32,
      child: TextButton(
        style: _style,
        onPressed: isLoading ? null : onPressed,
        child: isLoading
            ? const SizedBox(
                width: 16,
                height: 16,
                child: CircularProgressIndicator(strokeWidth: 2),
              )
            : Text(label),
      ),
    );
  }

  ButtonStyle get _style {
    switch (variant) {
      case AppButtonVariant.primary:
        return ButtonStyle(
          backgroundColor: WidgetStateProperty.all(AppColors.primary),
          foregroundColor: WidgetStateProperty.all(Colors.white),
          padding: WidgetStateProperty.all(
            size == AppButtonSize.md
                ? const EdgeInsets.symmetric(horizontal: 16, vertical: 8)
                : const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          ),
          shape: WidgetStateProperty.all(
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.sm)),
          ),
        );
      case AppButtonVariant.subtle:
        return ButtonStyle(
          backgroundColor: WidgetStateProperty.all(AppColors.primary.withOpacity(0.15)),
          foregroundColor: WidgetStateProperty.all(AppColors.primary),
          padding: WidgetStateProperty.all(
            size == AppButtonSize.md
                ? const EdgeInsets.symmetric(horizontal: 16, vertical: 8)
                : const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          ),
          shape: WidgetStateProperty.all(
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.sm)),
          ),
        );
      case AppButtonVariant.ghost:
        return ButtonStyle(
          foregroundColor: WidgetStateProperty.all(AppColors.primary),
          shape: WidgetStateProperty.all(
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.sm)),
          ),
        );
      case AppButtonVariant.destructive:
        return ButtonStyle(
          backgroundColor: WidgetStateProperty.all(AppColors.error),
          foregroundColor: WidgetStateProperty.all(Colors.white),
          padding: WidgetStateProperty.all(
            size == AppButtonSize.md
                ? const EdgeInsets.symmetric(horizontal: 16, vertical: 8)
                : const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          ),
          shape: WidgetStateProperty.all(
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.sm)),
          ),
        );
    }
  }
}
