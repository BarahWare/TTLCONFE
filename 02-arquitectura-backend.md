# EventOps — Arquitectura Backend

> Fuente: Sección 3 del Master Prompt
> Contexto para implementar la estructura del backend FastAPI, módulos y WebSockets.

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
