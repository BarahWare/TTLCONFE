# EventOps — Sistema de Roles y Permisos

> Fuente: Sección 6 del Master Prompt
> Contexto para implementar el sistema jerárquico de roles y permisos granulares.

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
