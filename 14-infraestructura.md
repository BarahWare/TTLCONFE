# EventOps — Infraestructura

> Fuente: Sección 16 del Master Prompt
> Contexto para implementar Docker, Nginx y deploy.

---

## 16. INFRAESTRUCTURA

### docker-compose.yml estructura

```yaml
services:
  api:
    build: ./backend
    environment:
      - DATABASE_URL
      - REDIS_URL
      - JWT_SECRET
    depends_on: [db, redis]

  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
      - "443:443"

  admin-web:
    build: ./admin-web
    depends_on: [api]

volumes:
  postgres_data:
```

### Nginx config (resumen)

- `/api/` → FastAPI backend
- `/ws/` → WebSocket upgrade
- `/` → Next.js admin web
- Cloudflare termina SSL, Nginx maneja internamente
