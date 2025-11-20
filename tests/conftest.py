"""Pytest configuration and fixtures."""

import shutil
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.models.base import Base

# Create test engine with PostgreSQL (NullPool avoids connection reuse issues in tests)
test_engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool,
)

# Create test session factory
TestAsyncSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
def initialize_cache():
    """Initialize FastAPICache for testing."""
    FastAPICache.init(InMemoryBackend(), prefix="test-cache")


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_uploads():
    """Clean up test upload directory before and after test session."""
    test_upload_dir = Path(settings.TEST_UPLOAD_DIR)

    # Clean up before tests
    if test_upload_dir.exists():
        shutil.rmtree(test_upload_dir)

    # Create fresh directory
    test_upload_dir.mkdir(parents=True, exist_ok=True)

    yield

    # Clean up after tests
    if test_upload_dir.exists():
        shutil.rmtree(test_upload_dir)


@pytest.fixture(autouse=True)
def use_test_upload_dir(monkeypatch):
    """Override UPLOAD_DIR to use TEST_UPLOAD_DIR for all tests."""
    # Monkeypatch the settings to use test upload directory
    monkeypatch.setattr(settings, "UPLOAD_DIR", settings.TEST_UPLOAD_DIR)

    # Also update the router's UPLOAD_DIR that was set at import time
    from app.files import router as files_router

    files_router.UPLOAD_DIR = Path(settings.TEST_UPLOAD_DIR)
    # Ensure the test directory exists
    files_router.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession]:
    """Create a fresh database for each test."""
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create a new session
    async with TestAsyncSessionLocal() as session:
        yield session

    # Drop all tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    """Create a test client with database session override."""

    async def override_get_db() -> AsyncGenerator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
