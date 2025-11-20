"""Filtering utilities."""

from typing import Any

from sqlalchemy import Select


class FilterParams:
    """Base class for filter parameters."""

    def apply(self, query: Select, model: Any) -> Select:
        """
        Apply filters to the query.

        Args:
            query: SQLAlchemy select statement
            model: SQLAlchemy model class

        Returns:
            Modified query with filters applied
        """
        for field_name, value in self.__dict__.items():
            if value is not None and hasattr(model, field_name):
                query = query.filter(getattr(model, field_name) == value)
        return query


class ItemFilterParams(FilterParams):
    """Filter parameters for items."""

    def __init__(
        self,
        title: str | None = None,
        is_active: bool | None = None,
    ):
        self.title = title
        self.is_active = is_active

    def apply(self, query: Select, model: Any) -> Select:
        """Apply item-specific filters."""
        if self.title is not None:
            query = query.filter(model.title.ilike(f"%{self.title}%"))
        if self.is_active is not None:
            query = query.filter(model.is_active == self.is_active)
        return query
