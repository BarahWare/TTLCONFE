# EventOps — Sistema de Diseño Flutter

> Fuente: Secciones 9-10 del Master Prompt
> Contexto para implementar design tokens, theme, widgets base reutilizables.

---

## 9. SISTEMA DE DISEÑO FLUTTER — DESIGN TOKENS

### 9.1 app_colors.dart

```dart
class AppColors {
  // Backgrounds
  static const background     = Color(0xFF0F1018);
  static const surface        = Color(0xFF1A1D2E);
  static const surfaceVariant = Color(0xFF15172A);

  // Accent
  static const primary        = Color(0xFFA855F7); // dark mode
  static const primaryLight   = Color(0xFF8B2ADB); // light mode

  // Text
  static const textPrimary    = Color(0xFFF0EDF5);
  // secondary: textPrimary.withOpacity(0.70)
  // tertiary:  textPrimary.withOpacity(0.45)

  // Borders
  static const outline        = Color(0x14FFFFFF); // white 8%

  // Semantic
  static const error          = Color(0xFFEF4444);
  static const success        = Color(0xFF22C55E);
  static const warning        = Color(0xFFF59E0B);
  static const gold           = Color(0xFFF0C040); // Master Trust shimmer
}
```

### 9.2 ThemeExtension — SemanticColors

```dart
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
  SemanticColors copyWith({...}) { ... }

  @override
  SemanticColors lerp(ThemeExtension<SemanticColors>? other, double t) { ... }
}
```

### 9.3 app_theme.dart — ThemeData

```dart
final darkTheme = ThemeData(
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
  extensions: [
    SemanticColors(
      success: AppColors.success,
      warning: AppColors.warning,
      gold: AppColors.gold,
      surfaceVariant: AppColors.surfaceVariant,
    ),
  ],
  textTheme: _buildTextTheme(),
  cardTheme: CardTheme(
    color: AppColors.surface,
    elevation: 0,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(6),
      side: BorderSide(color: AppColors.outline, width: 0.5),
    ),
  ),
  inputDecorationTheme: _buildInputTheme(),
);
```

### 9.4 Tipografía

- **Inter** (Google Fonts) — texto general
- **JetBrains Mono** — credenciales, IDs, tickets, IPs, código, datos técnicos

Escala de tamaños:
- `2xs` = 11px (labels, timestamps, badges)
- `xs` = 12px
- `sm` = 14px (body default)
- `md` = 18px
- `lg` = 24px

Pesos: 500 (medium) y 600 (semibold).

### 9.5 Radios y spacing

```dart
class AppRadius {
  static const xs = 4.0;
  static const sm = 6.0;  // cards
  static const md = 8.0;
  static const lg = 12.0;
}

class AppSpacing {
  static const xs  = 4.0;
  static const sm  = 8.0;
  static const md  = 16.0;
  static const lg  = 24.0;
  static const xl  = 32.0;
  static const xxl = 48.0;
}
```

---

## 10. WIDGETS BASE REUTILIZABLES

### AppScaffold — Sidebar + TopBar

```
┌─────────────────────────────────────────┐
│  TopBar (thin, border-bottom)           │
│  [☰]  EventOps         [🔔][👤]        │
├──────────┬──────────────────────────────┤
│          │                              │
│ Sidebar  │   Contenido principal        │
│ 224px    │   (flexible)                 │
│ (64px    │                              │
│ collapsed│                              │
│ )        │                              │
└──────────┴──────────────────────────────┘
```

- Sidebar: secciones agrupadas, ítem activo = fondo `primary.withOpacity(0.15)` + texto `primary`
- Íconos Lucide de 16px
- Colapsable con animación 200ms ease-out
- TopBar: borde inferior `outline`, acciones a la derecha

### AppCard

```dart
class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets? padding;
  final VoidCallback? onTap;
  // superficie #1A1D2E, borde 0.5px, radio 6, sin elevación
}
```

### AppButton — variantes

| Variante | Apariencia |
|---|---|
| `primary` | Fondo violeta sólido, texto blanco |
| `subtle` | Fondo `primary.withOpacity(0.15)`, texto violeta |
| `ghost` | Sin fondo, solo texto violeta |
| `destructive` | Fondo rojo |

Tamaños: `sm` (px12/py4) y `md` (px16/py8).

### AppBadge

Inline, padding pequeño, `BorderRadius.circular(4)`, texto 11px semibold.
Colores semánticos con fondo al 15% de opacidad.

### Chat bubbles

- **Usuario:** fondo violeta sólido, esquina inferior-derecha recortada
- **Asistente/Sistema:** fondo `white.withOpacity(0.08)`, borde tenue, esquina inferior-izquierda recortada
- Render de markdown con código en mono sobre `black.withOpacity(0.4)`
- Indicador "escribiendo": tres puntitos animados
