# EventOps — Estructura de la App Flutter

> Fuente: Sección 8 del Master Prompt
> Contexto para implementar la estructura del proyecto Flutter, state management y paquetes.

---

## 8. ESTRUCTURA DE LA APP FLUTTER

### 8.1 Estructura de carpetas

```
lib/
├── main.dart
├── app.dart
├── config/
│   └── env.dart
├── core/
│   ├── theme/
│   │   ├── app_theme.dart          # ThemeData dark + light
│   │   ├── app_colors.dart         # tokens de color
│   │   ├── app_typography.dart     # Inter + JetBrains Mono
│   │   ├── app_spacing.dart        # spacing tokens
│   │   └── theme_extensions.dart  # SemanticColors extension
│   ├── router/
│   │   └── app_router.dart         # GoRouter
│   ├── network/
│   │   ├── api_client.dart         # Dio + interceptors JWT
│   │   └── websocket_service.dart
│   ├── storage/
│   │   └── local_storage.dart      # Hive para offline cache
│   └── utils/
├── shared/
│   └── widgets/
│       ├── app_card.dart
│       ├── app_button.dart         # variantes: primary|subtle|ghost|destructive
│       ├── app_badge.dart
│       ├── app_scaffold.dart       # con sidebar colapsable + topbar
│       ├── app_input.dart
│       ├── app_avatar.dart
│       ├── app_modal.dart
│       └── app_toast.dart
├── features/
│   ├── auth/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   │       ├── login_screen.dart
│   │       └── auth_bloc.dart
│   ├── dashboard/
│   │   ├── presentation/
│   │   │   ├── dashboard_screen.dart
│   │   │   └── dashboard_bloc.dart
│   ├── schedule/
│   │   ├── presentation/
│   │   │   ├── my_schedule_screen.dart
│   │   │   ├── team_schedule_screen.dart
│   │   │   └── schedule_bloc.dart
│   ├── tasks/
│   ├── chat/
│   │   ├── presentation/
│   │   │   ├── channels_screen.dart
│   │   │   ├── chat_room_screen.dart
│   │   │   └── direct_message_screen.dart
│   ├── documents/
│   ├── inventory/
│   ├── teams/
│   ├── children/
│   ├── kitchen/
│   ├── sales/
│   ├── guests/
│   └── notifications/
```

### 8.2 State management

Usar **flutter_bloc** (BLoC pattern). Cada feature tiene su propio Bloc/Cubit.

### 8.3 Paquetes requeridos

```yaml
dependencies:
  flutter_bloc: ^8.x
  go_router: ^14.x
  dio: ^5.x
  hive_flutter: ^1.x
  google_fonts: ^6.x
  lucide_icons: ^1.x
  web_socket_channel: ^3.x
  flutter_local_notifications: ^17.x
  cached_network_image: ^3.x
  file_picker: ^8.x
  image_picker: ^1.x
  intl: ^0.19.x
  flutter_markdown: ^0.7.x
  shimmer: ^3.x
```
