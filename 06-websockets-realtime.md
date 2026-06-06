# EventOps — Arquitectura Realtime (WebSockets)

> Fuente: Sección 7 del Master Prompt
> Contexto para implementar la comunicación en tiempo real vía WebSockets.

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
