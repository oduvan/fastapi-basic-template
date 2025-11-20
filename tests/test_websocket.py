"""Tests for WebSocket endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestWebSocket:
    """Test WebSocket functionality."""

    async def test_websocket_test_page(self, client: AsyncClient):
        """Test WebSocket test page loads."""
        response = await client.get("/ws/test")
        assert response.status_code == 200
        assert "WebSocket" in response.text

    @pytest.mark.skip(reason="WebSocket testing requires different setup")
    async def test_websocket_connection(self, client: AsyncClient):
        """Test WebSocket connection.

        Note: This test is skipped as WebSocket testing requires
        a different testing approach with starlette.testclient.
        """
        pass
