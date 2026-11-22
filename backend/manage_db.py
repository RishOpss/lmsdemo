"""Create, drop, list or describe database tables.

Usage:
    python manage_db.py create [table ...]   # no table names = all tables
    python manage_db.py drop [table ...]     # no table names = all tables
    python manage_db.py list
    python manage_db.py describe <table>
"""
import asyncio
import sys

from sqlalchemy import Table, inspect

from app import models  # noqa: F401 (imports every model so metadata sees them)
from app.db.base import Base
from app.db.session import engine


def resolve_tables(names: list[str]) -> list[Table] | None:
    """Map table names to Table objects. Empty list -> None (meaning all tables)."""
    if not names:
        return None
    unknown = [n for n in names if n not in Base.metadata.tables]
    if unknown:
        known = ", ".join(sorted(Base.metadata.tables))
        sys.exit(f"Unknown table(s): {', '.join(unknown)}. Known tables: {known}")
    return [Base.metadata.tables[n] for n in names]


async def create_tables(names: list[str]) -> None:
    tables = resolve_tables(names)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, tables=tables)
    print("Tables created.")
    await list_tables()


async def drop_tables(names: list[str]) -> None:
    tables = resolve_tables(names)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, tables=tables)
    print("Tables dropped.")


async def list_tables() -> None:
    async with engine.connect() as conn:
        names = await conn.run_sync(lambda c: inspect(c).get_table_names())
    print("Tables in database:")
    for name in sorted(names):
        print(f"  - {name}")


async def describe_table(name: str) -> None:
    async with engine.connect() as conn:
        if not await conn.run_sync(lambda c: inspect(c).has_table(name)):
            sys.exit(f"Table '{name}' does not exist in the database.")
        columns = await conn.run_sync(lambda c: inspect(c).get_columns(name))
        pk = await conn.run_sync(lambda c: inspect(c).get_pk_constraint(name))
        fks = await conn.run_sync(lambda c: inspect(c).get_foreign_keys(name))

    pk_cols = set(pk.get("constrained_columns", []))
    print(f"Table: {name}")
    print(f"  {'column':<24}{'type':<24}{'nullable':<10}{'default'}")
    for c in columns:
        flag = " (PK)" if c["name"] in pk_cols else ""
        print(
            f"  {c['name'] + flag:<24}{str(c['type']):<24}"
            f"{'yes' if c['nullable'] else 'no':<10}{c['default'] or ''}"
        )
    for fk in fks:
        cols = ", ".join(fk["constrained_columns"])
        refs = ", ".join(fk["referred_columns"])
        print(f"  FK: {cols} -> {fk['referred_table']}({refs})")


async def main(action: str, args: list[str]) -> None:
    try:
        if action == "create":
            await create_tables(args)
        elif action == "drop":
            await drop_tables(args)
        elif action == "list":
            await list_tables()
        elif action == "describe":
            if len(args) != 1:
                sys.exit("Usage: python manage_db.py describe <table>")
            await describe_table(args[0])
        else:
            sys.exit(
                f"Unknown action '{action}'. Use 'create', 'drop', 'list' or 'describe'."
            )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2:]))
