# EventOps — Master Architecture & Build Prompt for OpenCode

> Este documento es el prompt maestro para construir **EventOps**, una plataforma integral de gestión operativa para conferencias y eventos. Combina la arquitectura técnica, el sistema de diseño Flutter, y todos los módulos operativos. OpenCode debe seguir este documento como fuente única de verdad.

---

## 1. VISIÓN DEL PRODUCTO

**EventOps** reemplaza el ecosistema disperso de WhatsApp, Excel, Google Drive y documentos sueltos por un único sistema operacional que centralice:

- Personas y roles jerárquicos
- Comunicación interna en tiempo real
- Documentación y repositorio de conocimiento
- Inventario por equipo
- Cronogramas y turnos flexibles
- Procesos y módulos especializados por área

La plataforma está orientada a **conferencias y eventos cristianos de gran escala** (cientos de voluntarios, múltiples días), pero diseñada para reutilizarse año tras año y adaptarse a cualquier tipo de congreso, retiro o encuentro masivo.

**No es** un CRM genérico. **No es** una red social. Es una plataforma operacional para coordinación en vivo.

---

## 2. STACK TECNOLÓGICO

| Capa | Tecnología |
|---|---|
| App móvil | Flutter (iOS + Android) |
| Admin web | Next.js + Tailwind CSS |
| Backend | Python FastAPI |
| Base de datos | PostgreSQL |
| Realtime | WebSockets |
| Cache / PubSub | Redis |
| Infraestructura | Docker Compose |
| Reverse proxy | Nginx |
| Hosting | AWS EC2 |
| CDN / DNS | Cloudflare |
| Auth | JWT con refresh tokens |
| Arquitectura | Modular monolith (NO microservices) |

---

## 3. ARQUITECTURA BACKEND

### 3.1 Estructura de carpetas

```
eventops/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── websockets/
│   │   ├── manager.py
│   │   └── handlers.py
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── schemas.py
│   │   │   └── models.py
│   │   ├── organizations/
│   │   ├── events/
│   │   ├── teams/
│   │   ├── users/
│   │   ├── roles/
│   │   ├── schedules/
│   │   ├── tasks/
│   │   ├── chat/
│   │   ├── documents/
│   │   ├── inventory/
│   │   ├── children/
│   │   ├── kitchen/
│   │   ├── sales/
│   │   ├── guests/
│   │   ├── notifications/
│   │   └── dashboards/
│   └── shared/
│       ├── models.py
│       ├── utils.py
│       └── exceptions.py
├── alembic/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
└── requirements.txt
```

### 3.2 Módulos FastAPI — cada módulo expone

- `router.py` — endpoints REST
- `service.py` — lógica de negocio
- `schemas.py` — Pydantic models (request/response)
- `models.py` — SQLAlchemy ORM models

### 3.3 WebSockets

El manager central en `websockets/manager.py` maneja:

- Conexión/desconexión por usuario y sala
- Broadcast a canales de equipo
- Mensajes directos
- Alertas de sistema en tiempo real
- Actualizaciones de cronograma en vivo

```python
# websockets/manager.py — estructura base
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.user_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, channel: str, user_id: int)
    async def disconnect(self, websocket: WebSocket, channel: str, user_id: int)
    async def broadcast_to_channel(self, channel: str, message: dict)
    async def send_to_user(self, user_id: int, message: dict)
    async def broadcast_event(self, event_id: int, message: dict)
```

---

## 4. SCHEMA DE BASE DE DATOS (PostgreSQL)

### 4.1 Entidades core

```sql
-- Organizations
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    logo_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Events
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    org_id INT REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    location VARCHAR(255),
    status VARCHAR(50) DEFAULT 'planning', -- planning|active|closed
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    org_id INT REFERENCES organizations(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    avatar_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Teams
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    name VARCHAR(255) NOT NULL,
    team_type VARCHAR(100) NOT NULL, -- sound|lighting|security|logistics|...
    description TEXT,
    color VARCHAR(7), -- hex color para UI
    icon VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    org_id INT REFERENCES organizations(id),
    name VARCHAR(100) NOT NULL, -- super_admin|event_director|team_leader|team_member|volunteer|viewer
    level INT NOT NULL, -- jerarquía numérica
    permissions JSONB DEFAULT '{}'
);

-- User-Team assignments
CREATE TABLE user_team_assignments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    team_id INT REFERENCES teams(id),
    role_id INT REFERENCES roles(id),
    event_id INT REFERENCES events(id),
    is_active BOOLEAN DEFAULT TRUE,
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, team_id, event_id)
);
```

### 4.2 Scheduling

```sql
CREATE TABLE schedules (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    team_id INT REFERENCES teams(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_datetime TIMESTAMPTZ NOT NULL,
    end_datetime TIMESTAMPTZ NOT NULL,
    location VARCHAR(255),
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_rule TEXT, -- iCal RRULE
    created_by INT REFERENCES users(id),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE schedule_assignments (
    id SERIAL PRIMARY KEY,
    schedule_id INT REFERENCES schedules(id),
    user_id INT REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'assigned', -- assigned|confirmed|absent
    notes TEXT
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    team_id INT REFERENCES teams(id),
    schedule_id INT REFERENCES schedules(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    scope TEXT,
    location VARCHAR(255),
    priority VARCHAR(20) DEFAULT 'normal', -- low|normal|high|critical
    status VARCHAR(50) DEFAULT 'pending', -- pending|in_progress|completed|cancelled
    due_datetime TIMESTAMPTZ,
    created_by INT REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE task_assignments (
    id SERIAL PRIMARY KEY,
    task_id INT REFERENCES tasks(id),
    user_id INT REFERENCES users(id),
    assigned_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.3 Chat

```sql
CREATE TABLE chat_channels (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    team_id INT REFERENCES teams(id), -- NULL = global
    name VARCHAR(255) NOT NULL,
    channel_type VARCHAR(50) DEFAULT 'team', -- team|direct|broadcast|alert
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    channel_id INT REFERENCES chat_channels(id),
    sender_id INT REFERENCES users(id),
    content TEXT,
    message_type VARCHAR(50) DEFAULT 'text', -- text|image|pdf|link|system
    file_url TEXT,
    is_pinned BOOLEAN DEFAULT FALSE,
    is_priority BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    edited_at TIMESTAMPTZ
);

CREATE TABLE direct_messages (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES users(id),
    receiver_id INT REFERENCES users(id),
    content TEXT,
    message_type VARCHAR(50) DEFAULT 'text',
    file_url TEXT,
    read_at TIMESTAMPTZ,
    sent_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.4 Documentación

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    team_id INT REFERENCES teams(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_url TEXT NOT NULL,
    file_type VARCHAR(50), -- pdf|image|doc|diagram|protocol
    file_size_bytes INT,
    tags TEXT[], -- array de tags
    category VARCHAR(100),
    uploaded_by INT REFERENCES users(id),
    version INT DEFAULT 1,
    is_public_to_event BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE document_search_index (
    id SERIAL PRIMARY KEY,
    document_id INT REFERENCES documents(id),
    content_text TEXT, -- texto extraído para FTS
    search_vector TSVECTOR
);
```

### 4.5 Inventario

```sql
CREATE TABLE inventory_categories (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(id),
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(50)
);

CREATE TABLE inventory_items (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    team_id INT REFERENCES teams(id),
    category_id INT REFERENCES inventory_categories(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INT DEFAULT 0,
    quantity_available INT DEFAULT 0,
    unit VARCHAR(50),
    status VARCHAR(50) DEFAULT 'available', -- available|in_use|maintenance|rented
    is_rented BOOLEAN DEFAULT FALSE,
    rental_supplier VARCHAR(255),
    assigned_location VARCHAR(255),
    responsible_user_id INT REFERENCES users(id),
    photo_url TEXT,
    serial_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE inventory_movements (
    id SERIAL PRIMARY KEY,
    item_id INT REFERENCES inventory_items(id),
    movement_type VARCHAR(50), -- checkout|checkin|transfer|adjustment
    quantity INT NOT NULL,
    from_location VARCHAR(255),
    to_location VARCHAR(255),
    performed_by INT REFERENCES users(id),
    notes TEXT,
    moved_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.6 Módulo Ministerio de Niños

```sql
CREATE TABLE children_classrooms (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    name VARCHAR(100) NOT NULL,
    capacity INT,
    age_range VARCHAR(50), -- "3-5 años"
    location VARCHAR(255),
    teacher_id INT REFERENCES users(id)
);

CREATE TABLE children_registry (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    classroom_id INT REFERENCES children_classrooms(id),
    child_name VARCHAR(255) NOT NULL,
    age INT,
    parent_name VARCHAR(255) NOT NULL,
    parent_phone VARCHAR(50) NOT NULL,
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(50),
    special_notes TEXT,
    registered_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE children_attendance (
    id SERIAL PRIMARY KEY,
    child_id INT REFERENCES children_registry(id),
    event_date DATE NOT NULL,
    checked_in_at TIMESTAMPTZ,
    checked_out_at TIMESTAMPTZ,
    checked_in_by INT REFERENCES users(id),
    checked_out_by INT REFERENCES users(id)
);

CREATE TABLE children_teaching_materials (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    classroom_id INT REFERENCES children_classrooms(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_url TEXT,
    lesson_date DATE,
    created_by INT REFERENCES users(id)
);
```

### 4.7 Módulo Cocina / Alimentación

```sql
CREATE TABLE kitchen_menus (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    name VARCHAR(255) NOT NULL,
    menu_date DATE NOT NULL,
    meal_type VARCHAR(50), -- breakfast|lunch|dinner|snack
    description TEXT,
    estimated_portions INT
);

CREATE TABLE kitchen_suppliers (
    id SERIAL PRIMARY KEY,
    org_id INT REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    category VARCHAR(100) -- verduras|carnes|lácteos|...
);

CREATE TABLE kitchen_ingredients (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    supplier_id INT REFERENCES kitchen_suppliers(id),
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    quantity_needed DECIMAL(10,2),
    quantity_in_stock DECIMAL(10,2) DEFAULT 0,
    unit_cost DECIMAL(10,2),
    notes TEXT
);

CREATE TABLE kitchen_purchase_orders (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    supplier_id INT REFERENCES kitchen_suppliers(id),
    order_date DATE,
    expected_delivery DATE,
    status VARCHAR(50) DEFAULT 'pending', -- pending|ordered|delivered|cancelled
    total_amount DECIMAL(10,2),
    notes TEXT,
    created_by INT REFERENCES users(id)
);

CREATE TABLE kitchen_tasks (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    menu_id INT REFERENCES kitchen_menus(id),
    title VARCHAR(255) NOT NULL,
    assigned_to INT REFERENCES users(id),
    scheduled_time TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'pending',
    notes TEXT
);
```

### 4.8 Módulo Stands de Ventas

```sql
CREATE TABLE sales_products (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(100),
    photo_url TEXT,
    sku VARCHAR(100)
);

CREATE TABLE sales_daily_stock (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES sales_products(id),
    stock_date DATE NOT NULL,
    opening_stock INT NOT NULL,
    current_stock INT,
    stand_location VARCHAR(100)
);

CREATE TABLE sales_transactions (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    product_id INT REFERENCES sales_products(id),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50), -- cash|transfer|debit|credit|pos
    pos_terminal_id VARCHAR(100),
    sold_by INT REFERENCES users(id),
    sold_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE sales_reconciliations (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    reconciliation_date DATE NOT NULL,
    total_cash DECIMAL(10,2) DEFAULT 0,
    total_transfer DECIMAL(10,2) DEFAULT 0,
    total_card DECIMAL(10,2) DEFAULT 0,
    total_reported DECIMAL(10,2),
    notes TEXT,
    closed_by INT REFERENCES users(id),
    closed_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.9 Módulo VIP / Recepción de Invitados

```sql
CREATE TABLE vip_guests (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    full_name VARCHAR(255) NOT NULL,
    title VARCHAR(100), -- Pastor, Dr., Minister...
    organization VARCHAR(255),
    languages TEXT[], -- ['español', 'inglés']
    email VARCHAR(255),
    phone VARCHAR(50),
    arrival_date DATE,
    departure_date DATE,
    hotel_name VARCHAR(255),
    room_number VARCHAR(50),
    seat_assignment VARCHAR(100),
    backstage_access BOOLEAN DEFAULT FALSE,
    transport_needed BOOLEAN DEFAULT FALSE,
    special_requirements TEXT,
    assigned_coordinator INT REFERENCES users(id),
    notes TEXT
);

CREATE TABLE vip_transport (
    id SERIAL PRIMARY KEY,
    guest_id INT REFERENCES vip_guests(id),
    transport_type VARCHAR(50), -- pickup|dropoff|internal
    datetime TIMESTAMPTZ,
    origin VARCHAR(255),
    destination VARCHAR(255),
    driver_name VARCHAR(255),
    driver_phone VARCHAR(50),
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT
);
```

### 4.10 Notificaciones

```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    event_id INT REFERENCES events(id),
    title VARCHAR(255) NOT NULL,
    body TEXT,
    notification_type VARCHAR(50), -- schedule_change|task_assigned|alert|announcement
    is_read BOOLEAN DEFAULT FALSE,
    related_entity_type VARCHAR(50), -- task|schedule|chat|inventory
    related_entity_id INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE push_tokens (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    token TEXT NOT NULL,
    platform VARCHAR(20), -- ios|android
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, token)
);
```

---

## 5. API DESIGN — ENDPOINTS PRINCIPALES

### Auth
```
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
POST   /api/v1/auth/register
GET    /api/v1/auth/me
PATCH  /api/v1/auth/me
```

### Organizations & Events
```
GET    /api/v1/organizations
POST   /api/v1/organizations
GET    /api/v1/organizations/{id}
GET    /api/v1/events
POST   /api/v1/events
GET    /api/v1/events/{id}
PATCH  /api/v1/events/{id}
GET    /api/v1/events/{id}/summary      # dashboard data
```

### Teams
```
GET    /api/v1/events/{event_id}/teams
POST   /api/v1/events/{event_id}/teams
GET    /api/v1/teams/{id}
PATCH  /api/v1/teams/{id}
POST   /api/v1/teams/{id}/members
DELETE /api/v1/teams/{id}/members/{user_id}
GET    /api/v1/teams/{id}/members
```

### Schedules & Tasks
```
GET    /api/v1/events/{event_id}/schedules
POST   /api/v1/events/{event_id}/schedules
PATCH  /api/v1/schedules/{id}
DELETE /api/v1/schedules/{id}
POST   /api/v1/schedules/{id}/assignments
GET    /api/v1/events/{event_id}/tasks
POST   /api/v1/events/{event_id}/tasks
PATCH  /api/v1/tasks/{id}
POST   /api/v1/tasks/{id}/assignments
GET    /api/v1/users/me/schedule         # cronograma personal
```

### Chat
```
GET    /api/v1/events/{event_id}/channels
POST   /api/v1/events/{event_id}/channels
GET    /api/v1/channels/{id}/messages
POST   /api/v1/channels/{id}/messages
GET    /api/v1/direct-messages/{user_id}
POST   /api/v1/direct-messages/{user_id}
WS     /ws/chat/{channel_id}?token={jwt}
WS     /ws/user/{user_id}?token={jwt}
```

### Documents
```
GET    /api/v1/teams/{team_id}/documents
POST   /api/v1/teams/{team_id}/documents
GET    /api/v1/documents/{id}
PATCH  /api/v1/documents/{id}
DELETE /api/v1/documents/{id}
GET    /api/v1/events/{event_id}/documents/search?q=&tag=&category=
```

### Inventory
```
GET    /api/v1/teams/{team_id}/inventory
POST   /api/v1/teams/{team_id}/inventory
PATCH  /api/v1/inventory/{id}
POST   /api/v1/inventory/{id}/movements
GET    /api/v1/inventory/{id}/history
GET    /api/v1/events/{event_id}/inventory/summary
```

### Módulos especializados
```
# Children Ministry
GET/POST  /api/v1/events/{event_id}/children/classrooms
GET/POST  /api/v1/children/classrooms/{id}/students
POST      /api/v1/children/students/{id}/attendance
GET       /api/v1/children/classrooms/{id}/materials

# Kitchen
GET/POST  /api/v1/events/{event_id}/kitchen/menus
GET/POST  /api/v1/events/{event_id}/kitchen/ingredients
GET/POST  /api/v1/events/{event_id}/kitchen/purchase-orders
GET/POST  /api/v1/events/{event_id}/kitchen/tasks

# Sales
GET/POST  /api/v1/events/{event_id}/sales/products
GET/POST  /api/v1/sales/products/{id}/stock
POST      /api/v1/events/{event_id}/sales/transactions
GET       /api/v1/events/{event_id}/sales/reconciliation
POST      /api/v1/events/{event_id}/sales/reconciliation/close

# Guests
GET/POST  /api/v1/events/{event_id}/guests
PATCH     /api/v1/guests/{id}
GET/POST  /api/v1/guests/{id}/transport

# Dashboards
GET       /api/v1/events/{event_id}/dashboard
GET       /api/v1/events/{event_id}/dashboard/teams
GET       /api/v1/events/{event_id}/dashboard/incidents
GET       /api/v1/events/{event_id}/dashboard/schedule-conflicts
```

---

## 6. SISTEMA DE ROLES Y PERMISOS

### Jerarquía de roles

| Nivel | Rol | Acceso |
|---|---|---|
| 1 | `super_admin` | Todo el sistema, todas las orgs |
| 2 | `event_director` | Todo el evento, todos los equipos |
| 3 | `team_leader` | Su equipo + reportes de su área |
| 4 | `team_member` | Operación de su equipo |
| 5 | `volunteer` | Solo lectura + sus tareas |
| 6 | `viewer` | Solo lectura |

### Permisos granulares (JSONB en DB)

```json
{
  "events": ["read", "write", "delete"],
  "teams": ["read", "write", "manage_members"],
  "schedules": ["read", "write", "delete", "assign"],
  "tasks": ["read", "write", "assign", "complete"],
  "chat": ["read", "write", "broadcast", "alert"],
  "documents": ["read", "upload", "delete"],
  "inventory": ["read", "write", "checkout", "admin"],
  "children": ["read", "write", "attendance"],
  "kitchen": ["read", "write", "orders"],
  "sales": ["read", "write", "reconcile"],
  "guests": ["read", "write", "full"],
  "dashboards": ["read"],
  "reports": ["read", "export"]
}
```

---

## 7. ARQUITECTURA REALTIME (WebSockets)

### Canales de eventos

```
ws://server/ws/chat/{channel_id}     → mensajes de equipo
ws://server/ws/user/{user_id}        → notificaciones personales
ws://server/ws/event/{event_id}      → actualizaciones globales del evento
```

### Tipos de mensajes WebSocket

```json
// Nuevo mensaje de chat
{ "type": "chat.message", "channel_id": 5, "payload": { ... } }

// Cambio en cronograma
{ "type": "schedule.updated", "schedule_id": 12, "payload": { ... } }

// Tarea asignada
{ "type": "task.assigned", "task_id": 34, "user_id": 7, "payload": { ... } }

// Alerta de prioridad
{ "type": "alert.priority", "from_user_id": 2, "payload": { "message": "...", "level": "critical" } }

// Anuncio general
{ "type": "announcement.broadcast", "event_id": 1, "payload": { ... } }

// Actualización de inventario
{ "type": "inventory.updated", "item_id": 22, "payload": { ... } }
```

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

---

## 11. ADMIN WEB (Next.js)

### Estructura de carpetas

```
admin-web/
├── app/
│   ├── (auth)/
│   │   └── login/
│   ├── (dashboard)/
│   │   ├── events/
│   │   ├── teams/
│   │   ├── users/
│   │   ├── schedules/
│   │   ├── inventory/
│   │   ├── documents/
│   │   ├── children/
│   │   ├── kitchen/
│   │   ├── sales/
│   │   ├── guests/
│   │   └── reports/
│   └── layout.tsx
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   └── TopBar.tsx
│   └── features/
├── lib/
│   ├── api.ts
│   ├── websocket.ts
│   └── auth.ts
└── tailwind.config.ts
```

Paleta Tailwind igual que Flutter: mismo sistema de colores, dark mode por defecto.

---

## 12. MÓDULOS OPERATIVOS — DETALLE COMPLETO

### 12.1 Sonido y Técnica
- Inventario: micrófonos, consolas, cables, adaptadores, parlantes (propios/alquilados)
- Documentación: cableado de escena, configuraciones de mezcla, procedimientos técnicos
- Turnos: operadores por día/sesión
- Historial de configuraciones reutilizables entre eventos

### 12.2 Iluminación
- Inventario de fixtures y controladores
- Documentación de escenas (presets)
- Protocolos operativos
- Turnos de operadores

### 12.3 Pantallas LED y Proyección
- Roles y turnos de operadores
- Documentación de procedimientos
- Configuraciones de software (resoluciones, señales)

### 12.4 Logística
- Inventario de elementos físicos: mesas, sillas, barreras, radios
- Ubicación de materiales en plano
- Préstamos y movimientos entre áreas
- Responsables por zona

### 12.5 Seguridad y Guardias
- Turnos por sector (puertas, pasillos, backstage, estacionamiento)
- Protocolos de emergencia (documentos adjuntos)
- Comunicaciones internas (canal propio en chat)
- Asignación de radios (vínculo con inventario)

### 12.6 Traductores
- Asignación a salas/sesiones
- Idiomas disponibles por voluntario
- Horarios y turnos
- Documentación de apoyo (glosarios, materiales previos)

### 12.7 Boletería y Acreditaciones
- Control de asistentes por sesión
- Validación de entradas/QR
- Tipos de acceso por categoría

### 12.8 Estacionamiento
- Sectores y capacidad
- Turnos de personal
- Incidencias

### 12.9 Médico / Emergencias
- Protocolos de respuesta
- Turno de guardia médica
- Registro de intervenciones (privado)
- Contactos de emergencia del evento

### 12.10 Limpieza
- Sectores asignados
- Turnos y rotaciones
- Checklist de estado por área

### 12.11 Stage Management
- Cue sheet del evento
- Cronograma de ensayos
- Coordinación con sonido/iluminación/LED
- Estado de piso en tiempo real

### 12.12 Coordinación de Voluntarios (transversal)
- Base de datos de voluntarios disponibles
- Disponibilidad por día/turno
- Asignación a equipos
- Registro de asistencia
- Historial de participación en eventos anteriores

---

## 13. DASHBOARDS OPERATIVOS

### Dashboard principal del evento

Widgets en tiempo real:
- Equipos activos / total de equipos
- Tareas pendientes / completadas / vencidas
- Incidencias abiertas
- Cumplimiento de cronograma (%)
- Conflictos de horario detectados
- Voluntarios presentes vs asignados
- Alertas de inventario (stock bajo, items sin devolver)
- Últimas actividades del chat

### Dashboard por equipo

- Estado de los miembros del equipo (presentes/ausentes)
- Tareas del equipo por estado
- Próximos turnos (siguiente hora)
- Inventario del equipo (resumen)
- Últimos documentos actualizados

### Dashboard de ventas (Sales stands)

- Ventas totales del día (por método de pago)
- Top productos por volumen
- Reconciliación pendiente / cerrada
- Stock crítico

### Dashboard de niños

- Total de niños por salón
- Estado de check-in del día actual
- Maestros asignados vs presentes

---

## 14. SOPORTE OFFLINE (Flutter)

Usar **Hive** como base local. Cache obligatorio:

| Entidad | TTL sugerido |
|---|---|
| Mi cronograma | Sincronización al iniciar |
| Mis tareas asignadas | Sincronización al iniciar |
| Documentos de mi equipo (metadata) | 24 hs |
| Mensajes recientes del canal | Últimas 100 mensajes |
| Inventario de mi equipo | 1 hora |

Estrategia:
- Al iniciar app: sync completo en background
- Sin conexión: mostrar datos cacheados con indicador "offline"
- Reconexión: push de cambios locales pendientes + pull de cambios remotos
- Conflictos: server wins por defecto, con aviso al usuario

---

## 15. NOTIFICACIONES

### Push (Flutter)

- Usar `flutter_local_notifications` + Firebase Cloud Messaging (FCM)
- Backend guarda push tokens en tabla `push_tokens`
- FastAPI envía push vía Firebase Admin SDK

### Tipos de notificación

| Tipo | Prioridad | Canal |
|---|---|---|
| Alerta crítica del director | MAX | Push + WebSocket + sonido |
| Tarea asignada | HIGH | Push + WebSocket |
| Cambio en mi turno | HIGH | Push + WebSocket |
| Nuevo mensaje directo | MEDIUM | Push + WebSocket |
| Nuevo mensaje de equipo | LOW | WebSocket (badge) |
| Anuncio general | MEDIUM | Push + WebSocket |
| Recordatorio de turno | MEDIUM | Push (15 min antes) |

---

## 16. INFRAESTRUCTURA

### docker-compose.yml estructura

```yaml
services:
  api:
    build: ./backend
    environment:
      - DATABASE_URL
      - REDIS_URL
      - JWT_SECRET
    depends_on: [db, redis]

  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
      - "443:443"

  admin-web:
    build: ./admin-web
    depends_on: [api]

volumes:
  postgres_data:
```

### Nginx config (resumen)

- `/api/` → FastAPI backend
- `/ws/` → WebSocket upgrade
- `/` → Next.js admin web
- Cloudflare termina SSL, Nginx maneja internamente

---

## 17. PLAN DE IMPLEMENTACIÓN MVP

### Fase 1 — Core (semanas 1-3)
1. Setup: Docker, PostgreSQL, FastAPI base, Nginx
2. Auth: registro, login, JWT, refresh tokens
3. Organizations y Events CRUD
4. Teams y roles
5. User-team assignments
6. App Flutter: pantalla de login, home básico con sidebar

### Fase 2 — Operación (semanas 4-6)
7. Schedules: CRUD, asignaciones, detección de conflictos
8. Tasks: CRUD, asignaciones, cambio de estado
9. WebSockets: manager, conexión desde Flutter
10. Chat: canales de equipo, mensajes directos
11. Push notifications básicas

### Fase 3 — Documentación e Inventario (semanas 7-9)
12. Documents: upload, tags, search
13. Inventory: items, movimientos, check-in/out
14. Dashboard operativo básico
15. App Flutter: pantallas de schedule, tasks, chat

### Fase 4 — Módulos especializados (semanas 10-14)
16. Ministerio de niños completo
17. Cocina y alimentación
18. Stands de ventas y reconciliación
19. VIP / Recepción de invitados
20. Dashboard avanzado con métricas en tiempo real

### Fase 5 — Pulido y producción (semanas 15-16)
21. Soporte offline (Hive cache)
22. Admin web Next.js completo
23. Testing E2E
24. Deploy a AWS EC2
25. Cloudflare DNS + SSL

---

## 18. CONVENCIONES DE CÓDIGO

### Backend Python
- PEP 8
- Type hints en todas las funciones
- Pydantic v2 para schemas
- SQLAlchemy 2.0 async
- Alembic para migraciones
- Naming: snake_case para todo

### Flutter
- Dart effective style
- BLoC: eventos en pasado (`UserLoaded`), estados descriptivos (`UserLoadSuccess`)
- Widgets: PascalCase
- Archivos: snake_case
- Separación estricta data/domain/presentation por feature
- Nunca lógica de negocio en widgets

### Base de datos
- Siempre `created_at TIMESTAMPTZ DEFAULT NOW()`
- Soft delete donde aplique: `deleted_at TIMESTAMPTZ`
- Índices en: FK columns, campos de búsqueda frecuente, `event_id` en todas las tablas operativas

---

## 19. CONSIDERACIONES DE SEGURIDAD

- JWT access token: 15 minutos de expiración
- JWT refresh token: 7 días, rotación en cada uso
- Passwords: bcrypt con salt rounds ≥ 12
- Rate limiting en endpoints de auth (Nginx + FastAPI middleware)
- Validación de permisos en cada endpoint (no solo en router)
- Upload de archivos: validar MIME type, limitar tamaño (max 50MB por archivo)
- WebSocket: autenticar token en handshake, no en mensaje
- CORS: solo orígenes autorizados

---

## 20. NOTAS FINALES PARA OPENCODE

- **Este documento es la fuente única de verdad.** Ante cualquier duda de implementación, consultá este archivo.
- El sistema es **modular monolith**, no microservices. Toda la lógica en un solo proceso FastAPI, separada internamente por módulos.
- El diseño visual Flutter sigue estrictamente los tokens de la sección 9. No improvisar colores ni radios.
- Cada módulo de la sección 12 es un equipo real con personas reales coordinando en vivo. Priorizar UX simple, acciones con pocos taps, feedback inmediato.
- La reutilización entre eventos es un objetivo clave: schedules, documentos e inventario se pueden clonar de un evento anterior.
- Ante cualquier feature nueva no documentada aquí, seguir el patrón establecido: módulo propio en backend, feature folder en Flutter, endpoints REST + WebSocket si necesita realtime.
