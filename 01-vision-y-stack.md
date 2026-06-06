# EventOps — Visión del Producto & Stack Tecnológico

> Fuente: Secciones 1-2 del Master Prompt
> Contexto completo para implementar la visión general y la arquitectura tecnológica de EventOps.

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
