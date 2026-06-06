import 'package:flutter/material.dart';

import 'app_colors.dart';
import 'app_typography.dart';

class SemanticColors extends ThemeExtension<SemanticColors> {
  final Color success;
  final Color warning;
  final Color gold;
  final Color surfaceVariant;

  const SemanticColors({
    required this.success,
    required this.warning,
    required this.gold,
    required this.surfaceVariant,
  });

  @override
  SemanticColors copyWith({
    Color? success,
    Color? warning,
    Color? gold,
    Color? surfaceVariant,
  }) {
    return SemanticColors(
      success: success ?? this.success,
      warning: warning ?? this.warning,
      gold: gold ?? this.gold,
      surfaceVariant: surfaceVariant ?? this.surfaceVariant,
    );
  }

  @override
  SemanticColors lerp(ThemeExtension<SemanticColors>? other, double t) {
    if (other is! SemanticColors) return this;
    return SemanticColors(
      success: Color.lerp(success, other.success, t)!,
      warning: Color.lerp(warning, other.warning, t)!,
      gold: Color.lerp(gold, other.gold, t)!,
      surfaceVariant: Color.lerp(surfaceVariant, other.surfaceVariant, t)!,
    );
  }
}

final ThemeData darkTheme = ThemeData(
  useMaterial3: true,
  brightness: Brightness.dark,
  scaffoldBackgroundColor: AppColors.background,
  colorScheme: const ColorScheme.dark(
    surface: AppColors.surface,
    primary: AppColors.primary,
    onSurface: AppColors.textPrimary,
    outline: AppColors.outline,
    error: AppColors.error,
  ),
  extensions: const [
    SemanticColors(
      success: AppColors.success,
      warning: AppColors.warning,
      gold: AppColors.gold,
      surfaceVariant: AppColors.surfaceVariant,
    ),
  ],
  textTheme: AppTypography.textTheme,
  cardTheme: CardTheme(
    color: AppColors.surface,
    elevation: 0,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(AppRadius.sm),
      side: const BorderSide(color: AppColors.outline, width: 0.5),
    ),
  ),
);
