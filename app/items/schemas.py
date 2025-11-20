"""Item schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    """Base item schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    is_active: bool = True


class ItemCreate(ItemBase):
    """Schema for creating an item."""

    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item."""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    is_active: bool | None = None


class ItemInDB(ItemBase):
    """Schema for item in database."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class Item(ItemInDB):
    """Schema for item response."""

    pass
