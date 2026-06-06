# EventOps — Admin Web (Next.js)

> Fuente: Sección 11 del Master Prompt
> Contexto para implementar el panel de administración web.

---

## 11. ADMIN WEB (Next.js)

### Estructura de carpetas

```
admin-web/
├── app/
│   ├── (auth)/
│   │   └── login/
│   ├── (dashboard)/
│   │   ├── events/
│   │   ├── teams/
│   │   ├── users/
│   │   ├── schedules/
│   │   ├── inventory/
│   │   ├── documents/
│   │   ├── children/
│   │   ├── kitchen/
│   │   ├── sales/
│   │   ├── guests/
│   │   └── reports/
│   └── layout.tsx
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   └── TopBar.tsx
│   └── features/
├── lib/
│   ├── api.ts
│   ├── websocket.ts
│   └── auth.ts
└── tailwind.config.ts
```

Paleta Tailwind igual que Flutter: mismo sistema de colores, dark mode por defecto.
