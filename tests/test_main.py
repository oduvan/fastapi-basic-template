"""Tests for main application endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestMainEndpoints:
    """Test main application endpoints."""

    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "version" in data

    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_docs_endpoint(self, client: AsyncClient):
        """Test API docs endpoint."""
        response = await client.get("/docs")
        assert response.status_code == 200

    async def test_redoc_endpoint(self, client: AsyncClient):
        """Test ReDoc endpoint."""
        response = await client.get("/redoc")
        assert response.status_code == 200
