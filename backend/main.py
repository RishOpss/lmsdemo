from contextlib import asynccontextmanager
from app import models  # noqa: F401 (load every model)
from fastapi import FastAPI
from sqlalchemy import text
import app.models  # noqa: F401 (load every model)
from app.db.session import engine
from fastapi.responses import HTMLResponse
from app.api.v1.router import api_router


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
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Course and Student API</title>
    </head>
    <body>
        <h1>Welcome to Course and Student API</h1>
        <p>Your FastAPI application is running successfully.</p>
        <a href="/docs">Explore API Documentation</a>
    </body>
    </html>
    """

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}