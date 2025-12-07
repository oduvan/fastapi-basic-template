"""Database models."""

from app.models.base import Base, TimestampMixin

__all__ = ["Base", "TimestampMixin"]


def get_all_models():
    """Import all models for Alembic migrations."""
    from app.items.models import Item, SubItem
    from app.blog.models import Category, Post

    return [Item, SubItem, Category, Post]
