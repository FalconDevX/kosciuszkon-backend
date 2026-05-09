from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routes.users import router as users_router
from app.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Creating database tables...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Tables created.")

    yield


app = FastAPI(
    title="Kościuszkon API",
    lifespan=lifespan
)

app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "FastAPI works"}