# EventOps — Schema de Base de Datos

> Fuente: Sección 4 del Master Prompt
> Contexto completo del esquema PostgreSQL para implementar todas las tablas.

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
