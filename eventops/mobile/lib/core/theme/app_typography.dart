import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTypography {
  AppTypography._();

  static TextTheme get textTheme {
    final inter = GoogleFonts.interTextTheme();
    return inter.copyWith(
      labelSmall: inter.labelSmall?.copyWith(
        fontFamily: 'JetBrains Mono',
        fontSize: 11,
        fontWeight: FontWeight.w600,
      ),
    );
  }
}
