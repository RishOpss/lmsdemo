from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models # noqa: F401 (imports every model, so create_all sees them)
from app.db.session import engine
from app.db.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop database tables (optional, for testing purposes)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
app = FastAPI(title = "LMS API", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}