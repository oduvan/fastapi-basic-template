"""Tests for items endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.items.models import Item


@pytest.mark.asyncio
class TestItemsCRUD:
    """Test CRUD operations for items."""

    async def test_create_item(self, client: AsyncClient):
        """Test creating an item."""
        item_data = {
            "title": "Test Item",
            "description": "Test Description",
            "is_active": True,
        }

        response = await client.post("/items/", json=item_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == item_data["title"]
        assert data["description"] == item_data["description"]
        assert data["is_active"] == item_data["is_active"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_read_items(self, client: AsyncClient, db_session: AsyncSession):
        """Test reading items with pagination."""
        # Create some test items
        for i in range(5):
            item = Item(
                title=f"Test Item {i}",
                description=f"Description {i}",
                is_active=True,
            )
            db_session.add(item)
        await db_session.commit()

        # Test default pagination
        response = await client.get("/items/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert data["total"] == 5
        assert len(data["items"]) == 5

        # Test pagination with page_size
        response = await client.get("/items/?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2

    async def test_read_item_by_id(self, client: AsyncClient, db_session: AsyncSession):
        """Test reading a single item by ID."""
        # Create a test item
        item = Item(
            title="Test Item",
            description="Test Description",
            is_active=True,
        )
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)

        response = await client.get(f"/items/{item.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item.id
        assert data["title"] == item.title

    async def test_read_nonexistent_item(self, client: AsyncClient):
        """Test reading a non-existent item."""
        response = await client.get("/items/999")
        assert response.status_code == 404

    async def test_update_item(self, client: AsyncClient, db_session: AsyncSession):
        """Test updating an item."""
        # Create a test item
        item = Item(
            title="Original Title",
            description="Original Description",
            is_active=True,
        )
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)

        # Update the item
        update_data = {"title": "Updated Title", "is_active": False}
        response = await client.put(f"/items/{item.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["is_active"] is False
        assert data["description"] == "Original Description"

    async def test_delete_item(self, client: AsyncClient, db_session: AsyncSession):
        """Test deleting an item."""
        # Create a test item
        item = Item(
            title="Test Item",
            description="Test Description",
            is_active=True,
        )
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)

        # Delete the item
        response = await client.delete(f"/items/{item.id}")
        assert response.status_code == 204

        # Verify item is deleted
        response = await client.get(f"/items/{item.id}")
        assert response.status_code == 404


@pytest.mark.asyncio
class TestItemsFiltering:
    """Test filtering and sorting for items."""

    async def test_filter_by_title(self, client: AsyncClient, db_session: AsyncSession):
        """Test filtering items by title."""
        # Create test items
        items = [
            Item(title="Apple", description="Fruit", is_active=True),
            Item(title="Banana", description="Fruit", is_active=True),
            Item(title="Cherry", description="Fruit", is_active=True),
        ]
        for item in items:
            db_session.add(item)
        await db_session.commit()

        response = await client.get("/items/?title=apple")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Apple"

    async def test_filter_by_is_active(self, client: AsyncClient, db_session: AsyncSession):
        """Test filtering items by active status."""
        # Create test items
        items = [
            Item(title="Active Item", description="Test", is_active=True),
            Item(title="Inactive Item", description="Test", is_active=False),
        ]
        for item in items:
            db_session.add(item)
        await db_session.commit()

        response = await client.get("/items/?is_active=false")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["is_active"] is False

    async def test_sorting(self, client: AsyncClient, db_session: AsyncSession):
        """Test sorting items."""
        # Create test items
        items = [
            Item(title="Zebra", description="Test", is_active=True),
            Item(title="Apple", description="Test", is_active=True),
            Item(title="Mango", description="Test", is_active=True),
        ]
        for item in items:
            db_session.add(item)
        await db_session.commit()

        response = await client.get("/items/?sort_by=title&sort_order=asc")
        assert response.status_code == 200
        data = response.json()
        titles = [item["title"] for item in data["items"]]
        assert titles == ["Apple", "Mango", "Zebra"]


@pytest.mark.asyncio
class TestItemsCaching:
    """Test caching for items endpoints."""

    async def test_item_caching(self, client: AsyncClient, db_session: AsyncSession):
        """Test that getting an item uses caching."""
        # Create a test item
        item = Item(
            title="Cached Item",
            description="Test caching",
            is_active=True,
        )
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)

        # First request (cache miss)
        response1 = await client.get(f"/items/{item.id}")
        assert response1.status_code == 200

        # Second request (should be cached)
        response2 = await client.get(f"/items/{item.id}")
        assert response2.status_code == 200
        assert response1.json() == response2.json()
