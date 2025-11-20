"""Pagination utilities."""

from typing import TypeVar

from pydantic import BaseModel, Field
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")

    @property
    def skip(self) -> int:
        """Calculate skip value for database query."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit value for database query."""
        return self.page_size


class PagedResponse[ModelType](BaseModel):
    """Paginated response."""

    items: list[ModelType]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(
        cls,
        items: list[ModelType],
        total: int,
        pagination: PaginationParams,
    ) -> PagedResponse[ModelType]:
        """Create paginated response."""
        total_pages = (total + pagination.page_size - 1) // pagination.page_size
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages,
        )


async def paginate(
    db: AsyncSession,
    query: Select,
    pagination: PaginationParams,
) -> tuple[list, int]:
    """
    Paginate a SQLAlchemy query.

    Args:
        db: Database session
        query: SQLAlchemy select statement
        pagination: Pagination parameters

    Returns:
        Tuple of (items, total_count)
    """
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Get paginated results
    paginated_query = query.offset(pagination.skip).limit(pagination.limit)
    result = await db.execute(paginated_query)
    items = list(result.scalars().all())

    return items, total
