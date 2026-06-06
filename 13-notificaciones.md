# EventOps — Notificaciones

> Fuente: Sección 15 del Master Prompt
> Contexto para implementar push notifications y sistema de alertas.

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
