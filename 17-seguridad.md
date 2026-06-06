# EventOps — Consideraciones de Seguridad

> Fuente: Sección 19 del Master Prompt
> Contexto para implementar seguridad en auth, API y datos.

---

## 19. CONSIDERACIONES DE SEGURIDAD

- JWT access token: 15 minutos de expiración
- JWT refresh token: 7 días, rotación en cada uso
- Passwords: bcrypt con salt rounds ≥ 12
- Rate limiting en endpoints de auth (Nginx + FastAPI middleware)
- Validación de permisos en cada endpoint (no solo en router)
- Upload de archivos: validar MIME type, limitar tamaño (max 50MB por archivo)
- WebSocket: autenticar token en handshake, no en mensaje
- CORS: solo orígenes autorizados
