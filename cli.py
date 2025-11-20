#!/usr/bin/env python3
"""CLI for FastAPI Basic Template."""

import asyncio

import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy import select

from app.core.config import settings
from app.core.database import AsyncSessionLocal, engine
from app.items.models import Item
from app.models.base import Base

app = typer.Typer(
    name="FastAPI CLI",
    help="Management commands for FastAPI Basic Template",
    add_completion=False,
)
console = Console()


@app.command()
def info():
    """Display application information."""
    table = Table(title="Application Information")
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("App Name", settings.APP_NAME)
    table.add_row("Version", settings.APP_VERSION)
    table.add_row("Environment", settings.ENVIRONMENT)
    table.add_row("Debug Mode", str(settings.DEBUG))
    table.add_row("Database URL", settings.DATABASE_URL)
    table.add_row("Redis URL", settings.REDIS_URL)

    console.print(table)


@app.command()
def create_db():
    """Create database tables."""

    async def _create():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        console.print("✅ Database tables created successfully!", style="green")

    asyncio.run(_create())


@app.command()
def drop_db():
    """Drop all database tables."""
    confirm = typer.confirm("⚠️  Are you sure you want to drop all tables?")
    if not confirm:
        console.print("❌ Operation cancelled", style="yellow")
        return

    async def _drop():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        console.print("✅ Database tables dropped successfully!", style="green")

    asyncio.run(_drop())


@app.command()
def seed_db(count: int = 10):
    """
    Seed database with sample data.

    Args:
        count: Number of items to create (default: 10)
    """

    async def _seed():
        async with AsyncSessionLocal() as session:
            # Create sample items
            for i in range(1, count + 1):
                item = Item(
                    title=f"Sample Item {i}",
                    description=f"This is sample item number {i}",
                    is_active=i % 2 == 0,
                )
                session.add(item)

            await session.commit()

        console.print(f"✅ Created {count} sample items successfully!", style="green")

    asyncio.run(_seed())


@app.command()
def list_items(limit: int = 10):
    """
    List items from the database.

    Args:
        limit: Maximum number of items to display (default: 10)
    """

    async def _list():
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Item).limit(limit))
            items = result.scalars().all()

            if not items:
                console.print("No items found in database", style="yellow")
                return

            table = Table(title=f"Items (showing {len(items)} of total)")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Title", style="magenta")
            table.add_column("Active", style="green")
            table.add_column("Created", style="blue")

            for item in items:
                table.add_row(
                    str(item.id),
                    item.title[:50],
                    "✓" if item.is_active else "✗",
                    item.created_at.strftime("%Y-%m-%d %H:%M"),
                )

            console.print(table)

    asyncio.run(_list())


@app.command()
def count_items():
    """Count total items in the database."""

    async def _count():
        async with AsyncSessionLocal() as session:
            from sqlalchemy import func

            result = await session.execute(select(func.count(Item.id)))
            count = result.scalar()
            console.print(f"Total items: {count}", style="cyan bold")

    asyncio.run(_count())


@app.command()
def clear_items():
    """Delete all items from the database."""
    confirm = typer.confirm("⚠️  Are you sure you want to delete all items?")
    if not confirm:
        console.print("❌ Operation cancelled", style="yellow")
        return

    async def _clear():
        async with AsyncSessionLocal() as session:
            await session.execute(Item.__table__.delete())
            await session.commit()
        console.print("✅ All items deleted successfully!", style="green")

    asyncio.run(_clear())


@app.command()
def shell():
    """Start an interactive Python shell with app context."""
    import code

    # Import commonly used modules for convenience
    from app.core.database import AsyncSessionLocal
    from app.items.models import Item

    local_vars = {
        "settings": settings,
        "AsyncSessionLocal": AsyncSessionLocal,
        "Item": Item,
        "asyncio": asyncio,
    }

    console.print("FastAPI Interactive Shell", style="bold cyan")
    console.print("Available objects:", style="yellow")
    for name in local_vars:
        console.print(f"  - {name}", style="green")

    code.interact(local=local_vars, banner="")


if __name__ == "__main__":
    app()
