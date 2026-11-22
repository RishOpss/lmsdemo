"""Create or drop all database tables.

Usage:
    python manage_db.py create
    python manage_db.py drop
    python manage_db.py list
"""
import asyncio
import sys

from sqlalchemy import inspect

from app import models  # noqa: F401 (imports every model so metadata sees them)
from app.db.base import Base
from app.db.session import engine


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")
    await list_tables()


async def drop_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("Tables dropped.")


async def list_tables() -> None:
    async with engine.connect() as conn:
        names = await conn.run_sync(lambda c: inspect(c).get_table_names())
    print("Tables in database:")
    for name in sorted(names):
        print(f"  - {name}")


async def main(action: str) -> None:
    try:
        if action == "create":
            await create_tables()
        elif action == "drop":
            await drop_tables()
        elif action == "list":
            await list_tables()
        else:
            sys.exit(f"Unknown action '{action}'. Use 'create', 'drop' or 'list'.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1]))
