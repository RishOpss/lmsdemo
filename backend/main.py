from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
import app.models  # noqa: F401 (load every model)
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify the database connection
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
        result = await conn.execute(text("SELECT 1"))
        print("Database says:", result.scalar())
    yield
    # Shutdown: close the connection pool
    await engine.dispose()

app = FastAPI(title="LMS API", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}
