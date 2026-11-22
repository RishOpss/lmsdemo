from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify the database connection
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    # Shutdown: close the connection pool
    await engine.dispose()


app = FastAPI(title="LMS API", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}
