# EventOps — Convenciones de Código

> Fuente: Sección 18 del Master Prompt
> Contexto para mantener consistencia en el código backend, Flutter y base de datos.

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
