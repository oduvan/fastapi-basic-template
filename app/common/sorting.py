"""Sorting utilities."""

from enum import Enum
from typing import Any

from sqlalchemy import Select, asc, desc


class SortOrder(str, Enum):
    """Sort order enum."""

    ASC = "asc"
    DESC = "desc"


class SortParams:
    """Sorting parameters."""

    def __init__(
        self,
        sort_by: str | None = None,
        sort_order: SortOrder = SortOrder.ASC,
    ):
        self.sort_by = sort_by
        self.sort_order = sort_order

    def apply(self, query: Select, model: Any) -> Select:
        """
        Apply sorting to the query.

        Args:
            query: SQLAlchemy select statement
            model: SQLAlchemy model class

        Returns:
            Modified query with sorting applied
        """
        if self.sort_by and hasattr(model, self.sort_by):
            field = getattr(model, self.sort_by)
            if self.sort_order == SortOrder.DESC:
                query = query.order_by(desc(field))
            else:
                query = query.order_by(asc(field))
        return query


class ItemSortParams(SortParams):
    """Sorting parameters for items."""

    def __init__(
        self,
        sort_by: str | None = "created_at",
        sort_order: SortOrder = SortOrder.DESC,
    ):
        super().__init__(sort_by, sort_order)
