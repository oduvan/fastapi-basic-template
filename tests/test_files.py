"""Tests for file upload/download endpoints."""

import io

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestFileOperations:
    """Test file upload, download, and deletion."""

    async def test_upload_file(self, client: AsyncClient):
        """Test uploading a file."""
        file_content = b"This is a test file content"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}

        response = await client.post("/files/upload", files=files)

        assert response.status_code == 201
        data = response.json()
        assert "filename" in data
        assert "size" in data
        assert data["size"] == len(file_content)
        assert data["message"] == "File uploaded successfully"

    async def test_upload_file_without_filename(self, client: AsyncClient):
        """Test uploading a file without a filename."""
        file_content = b"Test content"
        files = {"file": ("", io.BytesIO(file_content), "text/plain")}

        response = await client.post("/files/upload", files=files)

        # FastAPI returns 422 for validation errors, but the endpoint logic returns 400
        # The empty filename is caught by the endpoint logic
        assert response.status_code in [400, 422]

    async def test_list_files(self, client: AsyncClient):
        """Test listing uploaded files."""
        # Upload a test file first
        file_content = b"Test content"
        files = {"file": ("test_list.txt", io.BytesIO(file_content), "text/plain")}
        await client.post("/files/upload", files=files)

        # List files
        response = await client.get("/files/list")

        assert response.status_code == 200
        data = response.json()
        assert "files" in data
        assert "total" in data
        assert data["total"] >= 1

    async def test_download_file(self, client: AsyncClient):
        """Test downloading a file."""
        # Upload a test file first
        file_content = b"Download test content"
        files = {"file": ("test_download.txt", io.BytesIO(file_content), "text/plain")}
        upload_response = await client.post("/files/upload", files=files)
        filename = upload_response.json()["filename"]

        # Download the file
        response = await client.get(f"/files/download/{filename}")

        assert response.status_code == 200
        assert response.content == file_content

    async def test_download_nonexistent_file(self, client: AsyncClient):
        """Test downloading a non-existent file."""
        response = await client.get("/files/download/nonexistent.txt")
        assert response.status_code == 404

    async def test_delete_file(self, client: AsyncClient):
        """Test deleting a file."""
        # Upload a test file first
        file_content = b"Delete test content"
        files = {"file": ("test_delete.txt", io.BytesIO(file_content), "text/plain")}
        upload_response = await client.post("/files/upload", files=files)
        filename = upload_response.json()["filename"]

        # Delete the file
        response = await client.delete(f"/files/{filename}")
        assert response.status_code == 204

        # Verify file is deleted
        download_response = await client.get(f"/files/download/{filename}")
        assert download_response.status_code == 404

    async def test_delete_nonexistent_file(self, client: AsyncClient):
        """Test deleting a non-existent file."""
        response = await client.delete("/files/nonexistent.txt")
        assert response.status_code == 404
