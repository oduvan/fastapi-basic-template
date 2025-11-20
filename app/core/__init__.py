"""Core application module."""

from app.core.config import settings
from app.core.database import engine, get_db

__all__ = ["engine", "get_db", "settings"]
