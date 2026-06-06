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


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
