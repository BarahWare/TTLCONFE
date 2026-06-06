# EventOps — API Endpoints

> Fuente: Sección 5 del Master Prompt
> Contexto para implementar todos los endpoints REST de la API.

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
