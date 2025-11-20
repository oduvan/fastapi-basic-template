"""Item service for business logic."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.filtering import ItemFilterParams
from app.common.pagination import PaginationParams, paginate
from app.common.sorting import ItemSortParams
from app.items.models import Item as ItemModel
from app.items.schemas import ItemCreate, ItemUpdate


class ItemService:
    """Service for item operations."""

    @staticmethod
    async def get(db: AsyncSession, item_id: int) -> ItemModel | None:
        """Get item by ID."""
        result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi(
        db: AsyncSession,
        pagination: PaginationParams | None = None,
        filters: ItemFilterParams | None = None,
        sort: ItemSortParams | None = None,
    ) -> tuple[list[ItemModel], int]:
        """
        Get multiple items with pagination, filtering, and sorting.

        Returns tuple of (items, total_count).
        """
        query = select(ItemModel)

        # Apply filters
        if filters:
            query = filters.apply(query, ItemModel)

        # Apply sorting
        if sort:
            query = sort.apply(query, ItemModel)

        # Apply pagination
        if pagination:
            items, total = await paginate(db, query, pagination)
            return items, total

        # Fallback to simple query
        result = await db.execute(query)
        items = list(result.scalars().all())
        return items, len(items)

    @staticmethod
    async def create(db: AsyncSession, item_in: ItemCreate) -> ItemModel:
        """Create new item."""
        db_item = ItemModel(**item_in.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def update(db: AsyncSession, item_id: int, item_in: ItemUpdate) -> ItemModel | None:
        """Update item."""
        result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
        db_item = result.scalar_one_or_none()

        if not db_item:
            return None

        update_data = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)

        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def delete(db: AsyncSession, item_id: int) -> bool:
        """Delete item."""
        result = await db.execute(select(ItemModel).filter(ItemModel.id == item_id))
        db_item = result.scalar_one_or_none()

        if not db_item:
            return False

        await db.delete(db_item)
        await db.commit()
        return True
