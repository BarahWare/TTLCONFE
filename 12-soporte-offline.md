# EventOps — Soporte Offline (Flutter)

> Fuente: Sección 14 del Master Prompt
> Contexto para implementar caché offline con Hive.

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
