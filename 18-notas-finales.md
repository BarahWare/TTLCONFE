# EventOps — Notas Finales para OpenCode

> Fuente: Sección 20 del Master Prompt
> Instrucciones finales para que OpenCode implemente correctamente.

---

## 20. NOTAS FINALES PARA OPENCODE

- **Este documento es la fuente única de verdad.** Ante cualquier duda de implementación, consultá este archivo.
- El sistema es **modular monolith**, no microservices. Toda la lógica en un solo proceso FastAPI, separada internamente por módulos.
- El diseño visual Flutter sigue estrictamente los tokens de la sección 9. No improvisar colores ni radios.
- Cada módulo de la sección 12 es un equipo real con personas reales coordinando en vivo. Priorizar UX simple, acciones con pocos taps, feedback inmediato.
- La reutilización entre eventos es un objetivo clave: schedules, documentos e inventario se pueden clonar de un evento anterior.
- Ante cualquier feature nueva no documentada aquí, seguir el patrón establecido: módulo propio en backend, feature folder en Flutter, endpoints REST + WebSocket si necesita realtime.
