"""Tests for HTML pages with form validation."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_index_page(client: AsyncClient):
    """Test index page loads successfully."""
    response = await client.get("/pages/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_contact_form_get(client: AsyncClient):
    """Test contact form GET request."""
    response = await client.get("/pages/contact")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert b"Contact Form" in response.content


@pytest.mark.asyncio
async def test_contact_form_valid_submission(client: AsyncClient):
    """Test valid contact form submission."""
    form_data = {
        "name": "John Doe",
        "email": "JOHN@EXAMPLE.COM",  # Test email lowercase conversion
        "message": "This is a test message",
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 200
    assert b"Success!" in response.content
    assert b"john@example.com" in response.content  # Verify lowercase


@pytest.mark.asyncio
async def test_contact_form_invalid_email(client: AsyncClient):
    """Test contact form with invalid email."""
    form_data = {
        "name": "John Doe",
        "email": "not-an-email",
        "message": "Test message",
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    assert b"Validation Error!" in response.content
    assert b"Invalid email format" in response.content


@pytest.mark.asyncio
async def test_contact_form_missing_at_in_email(client: AsyncClient):
    """Test contact form with email missing @ symbol."""
    form_data = {
        "name": "John Doe",
        "email": "emailexample.com",
        "message": "Test message",
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    assert b"Invalid email format" in response.content


@pytest.mark.asyncio
async def test_contact_form_empty_name(client: AsyncClient):
    """Test contact form with empty name."""
    form_data = {
        "name": "",
        "email": "john@example.com",
        "message": "Test message",
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    assert b"Validation Error!" in response.content


@pytest.mark.asyncio
async def test_contact_form_empty_email(client: AsyncClient):
    """Test contact form with empty email."""
    form_data = {
        "name": "John Doe",
        "email": "",
        "message": "Test message",
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    assert b"Validation Error!" in response.content


@pytest.mark.asyncio
async def test_contact_form_empty_message(client: AsyncClient):
    """Test contact form with empty message."""
    form_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "",
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    assert b"Validation Error!" in response.content


@pytest.mark.asyncio
async def test_contact_form_name_too_long(client: AsyncClient):
    """Test contact form with name exceeding max length."""
    form_data = {
        "name": "x" * 101,  # Max is 100
        "email": "john@example.com",
        "message": "Test message",
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    assert b"Validation Error!" in response.content


@pytest.mark.asyncio
async def test_contact_form_email_too_long(client: AsyncClient):
    """Test contact form with email exceeding max length."""
    form_data = {
        "name": "John Doe",
        "email": "x" * 250 + "@test.com",  # Max is 255
        "message": "Test message",
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    assert b"Validation Error!" in response.content


@pytest.mark.asyncio
async def test_contact_form_message_too_long(client: AsyncClient):
    """Test contact form with message exceeding max length."""
    form_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "x" * 1001,  # Max is 1000
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    assert b"Validation Error!" in response.content


@pytest.mark.asyncio
async def test_contact_form_preserves_values_on_error(client: AsyncClient):
    """Test that form values are preserved when validation fails."""
    form_data = {
        "name": "John Doe",
        "email": "invalid-email",
        "message": "Test message",
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    # Verify form data is preserved
    assert b"John Doe" in response.content
    assert b"invalid-email" in response.content
    assert b"Test message" in response.content


@pytest.mark.asyncio
async def test_contact_form_multiple_validation_errors(client: AsyncClient):
    """Test contact form with multiple validation errors."""
    form_data = {
        "name": "",  # Empty
        "email": "not-an-email",  # Invalid
        "message": "",  # Empty
    }
    response = await client.post("/pages/contact", data=form_data)
    assert response.status_code == 422
    assert b"Validation Error!" in response.content
