"""HTML pages with Jinja2 templates."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.items.service import ItemService
from app.pages.schemas import ContactForm

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Home page demonstrating Jinja2 templates with PostCSS styles.
    """
    # Get some recent items to display
    items, _ = await ItemService.get_multi(db)
    items = items[:5]  # Limit to 5 most recent

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Home",
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "items": items,
        },
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact_form(request: Request):
    """Display contact form."""
    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "title": "Contact",
            "app_name": settings.APP_NAME,
        },
    )


@router.post("/contact", response_class=HTMLResponse)
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    """Handle contact form submission with validation."""
    # Base context for template
    context = {
        "request": request,
        "title": "Contact",
        "app_name": settings.APP_NAME,
    }
    status_code = 200

    # Validate form data
    try:
        form_data = ContactForm(name=name, email=email, message=message)
        # Here you would typically save to DB, send email, etc.
        context["success"] = True
        context["submitted_data"] = {
            "name": form_data.name,
            "email": form_data.email,
            "message": form_data.message,
        }
    except ValidationError as e:
        # Parse validation errors
        errors = {}
        for error in e.errors():
            field = error["loc"][0]
            errors[field] = error["msg"]

        context["errors"] = errors
        context["form_data"] = {
            "name": name,
            "email": email,
            "message": message,
        }
        status_code = 422

    return templates.TemplateResponse("contact.html", context, status_code=status_code)
