"""Items API router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.filtering import ItemFilterParams
from app.common.pagination import PagedResponse, PaginationParams
from app.common.sorting import ItemSortParams, SortOrder
from app.core.database import get_db
from app.items import constants
from app.items.dependencies import limiter
from app.items.exceptions import ItemNotFoundException
from app.items.schemas import Item, ItemCreate, ItemUpdate
from app.items.service import ItemService

router = APIRouter()


@router.get("/", response_model=PagedResponse[Item])
async def read_items(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    title: Annotated[str | None, Query()] = None,
    is_active: Annotated[bool | None, Query()] = None,
    sort_by: Annotated[str | None, Query()] = "created_at",
    sort_order: Annotated[SortOrder, Query()] = SortOrder.DESC,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve items with pagination, filtering, and sorting.

    **Pagination:**
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)

    **Filtering:**
    - **title**: Filter by title (case-insensitive partial match)
    - **is_active**: Filter by active status

    **Sorting:**
    - **sort_by**: Field to sort by (default: created_at)
    - **sort_order**: Sort order (asc/desc, default: desc)
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    filters = ItemFilterParams(title=title, is_active=is_active)
    sort = ItemSortParams(sort_by=sort_by, sort_order=sort_order)

    items, total = await ItemService.get_multi(
        db, pagination=pagination, filters=filters, sort=sort
    )

    return PagedResponse.create(items=items, total=total, pagination=pagination)


@router.get("/{item_id}", response_model=Item)
@cache(expire=constants.ITEM_CACHE_EXPIRE_SECONDS)
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get item by ID (cached).

    - **item_id**: ID of the item to retrieve

    This endpoint demonstrates Redis caching with fastapi-cache2.
    """
    item = await ItemService.get(db, item_id=item_id)
    if not item:
        raise ItemNotFoundException(item_id=item_id)
    return item


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
@limiter.limit(constants.ITEM_CREATE_RATE_LIMIT)
async def create_item(
    request: Request,
    item_in: ItemCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create new item (rate limited).

    - **title**: Item title (required)
    - **description**: Item description (optional)
    - **is_active**: Whether the item is active (default: true)

    This endpoint demonstrates rate limiting with slowapi.
    """
    item = await ItemService.create(db, item_in=item_in)
    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an item.

    - **item_id**: ID of the item to update
    - **title**: New title (optional)
    - **description**: New description (optional)
    - **is_active**: New active status (optional)
    """
    item = await ItemService.update(db, item_id=item_id, item_in=item_in)
    if not item:
        raise ItemNotFoundException(item_id=item_id)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an item.

    - **item_id**: ID of the item to delete
    """
    deleted = await ItemService.delete(db, item_id=item_id)
    if not deleted:
        raise ItemNotFoundException(item_id=item_id)
