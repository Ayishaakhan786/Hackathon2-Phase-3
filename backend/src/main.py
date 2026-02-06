from fastapi import FastAPI
from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.tasks import router as tasks_router
from src.api.health import router as health_router  # Import health router
from src.core.config import settings
from contextlib import asynccontextmanager
from src.core.database import engine
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Clean up code here (if needed)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Include health check routers first
app.include_router(health_router, prefix="", tags=["health"])  # Health endpoints at root level

# Include API routers
app.include_router(auth_router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(users_router, prefix=settings.API_V1_STR + "/users", tags=["users"])
app.include_router(tasks_router, prefix=settings.API_V1_STR + "/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management API"}