from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.modules.auth.router import router as auth_router
from app.modules.organizations.router import router as organizations_router
from app.modules.events.router import router as events_router
from app.modules.teams.router import router as teams_router
from app.modules.roles.router import router as roles_router
from app.modules.users.router import router as users_router
from app.modules.schedules.router import router as schedules_router
from app.modules.tasks.router import router as tasks_router
from app.websockets.handlers import router as ws_router
from app.modules.chat.router import router as chat_router
from app.modules.documents.router import router as documents_router
from app.modules.inventory.router import router as inventory_router
from app.modules.notifications.router import router as notifications_router
from app.modules.dashboards.router import router as dashboards_router
from app.modules.children.router import router as children_router
from app.modules.kitchen.router import router as kitchen_router
from app.modules.sales.router import router as sales_router
from app.modules.guests.router import router as guests_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="EventOps", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(organizations_router)
app.include_router(events_router)
app.include_router(teams_router)
app.include_router(roles_router)
app.include_router(users_router)
app.include_router(schedules_router)
app.include_router(tasks_router)
app.include_router(ws_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(inventory_router)
app.include_router(notifications_router)
app.include_router(dashboards_router)
app.include_router(children_router)
app.include_router(kitchen_router)
app.include_router(sales_router)
app.include_router(guests_router)


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
