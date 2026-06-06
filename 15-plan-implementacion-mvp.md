# EventOps — Plan de Implementación MVP

> Fuente: Sección 17 del Master Prompt
> Contexto para ejecutar el plan de desarrollo en fases.

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
