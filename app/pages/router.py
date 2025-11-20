"""HTML pages with Jinja2 templates."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.items.service import ItemService

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
