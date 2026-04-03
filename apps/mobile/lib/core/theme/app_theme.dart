import 'package:flutter/material.dart';

ThemeData buildAppTheme() {
  const canvas = Color(0xFF12100F);
  const surface = Color(0xFF1B1715);
  const elevated = Color(0xFF27211E);
  const ink = Color(0xFFF6EDE2);
  const muted = Color(0xFFBCAEA2);
  const accent = Color(0xFFD18C5B);
  const secondary = Color(0xFF71917A);
  const outline = Color(0xFF3A302B);

  final scheme =
      ColorScheme.fromSeed(
        seedColor: accent,
        brightness: Brightness.dark,
      ).copyWith(
        primary: accent,
        secondary: secondary,
        surface: surface,
        onSurface: ink,
        outline: outline,
      );

  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: canvas,
    cardTheme: CardThemeData(
      color: elevated,
      elevation: 0,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(28),
        side: const BorderSide(color: outline),
      ),
    ),
    textTheme: const TextTheme(
      displayLarge: TextStyle(
        fontSize: 42,
        fontWeight: FontWeight.w700,
        height: 0.96,
        color: ink,
        letterSpacing: -1.3,
      ),
      headlineMedium: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.w700,
        color: ink,
        letterSpacing: -0.4,
      ),
      titleMedium: TextStyle(
        fontSize: 16,
        fontWeight: FontWeight.w700,
        color: ink,
      ),
      bodyLarge: TextStyle(fontSize: 15, height: 1.55, color: ink),
      bodyMedium: TextStyle(fontSize: 13, height: 1.5, color: muted),
      labelLarge: TextStyle(
        fontSize: 12,
        fontWeight: FontWeight.w700,
        letterSpacing: 0.8,
        color: ink,
      ),
    ),
    chipTheme: ChipThemeData(
      backgroundColor: elevated,
      selectedColor: accent.withOpacity(0.15),
      disabledColor: elevated,
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 2),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(999),
        side: const BorderSide(color: outline),
      ),
      labelStyle: const TextStyle(
        fontSize: 11,
        fontWeight: FontWeight.w600,
        color: ink,
      ),
      side: const BorderSide(color: outline),
    ),
  );
}
