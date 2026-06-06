import 'package:flutter/material.dart';

class AppColors {
  AppColors._();

  static const Color background = Color(0xFF0F1018);
  static const Color surface = Color(0xFF1A1D2E);
  static const Color surfaceVariant = Color(0xFF15172A);

  static const Color primary = Color(0xFFA855F7);
  static const Color primaryLight = Color(0xFF8B2ADB);

  static const Color textPrimary = Color(0xFFF0EDF5);
  static Color get textSecondary => textPrimary.withOpacity(0.70);
  static Color get textTertiary => textPrimary.withOpacity(0.45);

  static const Color outline = Color(0x14FFFFFF);

  static const Color error = Color(0xFFEF4444);
  static const Color success = Color(0xFF22C55E);
  static const Color warning = Color(0xFFF59E0B);
  static const Color gold = Color(0xFFF0C040);
}
