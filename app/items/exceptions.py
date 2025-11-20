"""Items domain exceptions."""

from fastapi import HTTPException, status


class ItemNotFoundException(HTTPException):
    """Exception raised when item is not found."""

    def __init__(self, item_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
