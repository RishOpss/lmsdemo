from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, echo=settings.SQL_ECHO, future=True)

