"""Tests for background tasks endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestBackgroundTasks:
    """Test background tasks functionality."""

    async def test_send_email_task(self, client: AsyncClient):
        """Test sending email in background."""
        email_data = {
            "to": "test@example.com",
            "subject": "Test Email",
            "body": "This is a test email",
        }

        response = await client.post("/tasks/send-email", json=email_data)

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Email task queued successfully"
        assert data["to"] == email_data["to"]
        assert data["status"] == "processing"

    async def test_process_data_task(self, client: AsyncClient):
        """Test data processing in background."""
        request_data = {"data": [1, 2, 3, 4, 5], "operation": "sum"}

        response = await client.post("/tasks/process-data", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Data processing task queued successfully"
        assert data["operation"] == "sum"
        assert data["data_size"] == 5
        assert data["status"] == "processing"

    async def test_log_task(self, client: AsyncClient):
        """Test logging in background."""
        response = await client.post("/tasks/log", params={"message": "Test log message"})

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Log task queued successfully"
        assert data["status"] == "processing"

    async def test_multiple_tasks(self, client: AsyncClient):
        """Test multiple background tasks."""
        response = await client.post("/tasks/multiple-tasks")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Multiple tasks queued successfully"
        assert data["tasks_count"] == 4
        assert data["status"] == "processing"
