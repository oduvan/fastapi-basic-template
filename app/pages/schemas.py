"""Pydantic schemas for page forms."""

import re

from fastapi import Form
from pydantic import BaseModel, Field, field_validator


class ContactForm(BaseModel):
    """Contact form validation schema."""

    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=255)
    message: str = Field(..., min_length=1, max_length=1000)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format using regex."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v.lower()

    @classmethod
    def as_form(
        cls,
        name: str = Form(..., min_length=1, max_length=100),
        email: str = Form(..., max_length=255),
        message: str = Form(..., min_length=1, max_length=1000),
    ) -> ContactForm:
        """Create form instance from Form data."""
        return cls(name=name, email=email, message=message)
