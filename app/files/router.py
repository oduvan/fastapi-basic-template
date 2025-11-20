"""File upload/download endpoints."""

import os
from pathlib import Path
from typing import Annotated

import aiofiles
from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Ensure upload directory exists
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # Rate limit: 5 uploads per minute
async def upload_file(
    request: Request,
    file: Annotated[UploadFile, File(description="File to upload")],
):
    """
    Upload a file (rate limited to 5 uploads per minute).

    - **file**: File to upload (max size: 10MB)

    Returns the filename and file size.
    This endpoint demonstrates rate limiting for resource-intensive operations.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided",
        )

    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes",
        )

    # Generate safe filename
    filename = file.filename
    file_path = UPLOAD_DIR / filename

    # If file exists, add number suffix
    counter = 1
    while file_path.exists():
        name, ext = os.path.splitext(filename)
        file_path = UPLOAD_DIR / f"{name}_{counter}{ext}"
        counter += 1

    # Save file
    try:
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {e!s}",
        ) from e

    return {
        "filename": file_path.name,
        "size": file_size,
        "content_type": file.content_type,
        "message": "File uploaded successfully",
    }


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a file.

    - **filename**: Name of the file to download
    """
    file_path = UPLOAD_DIR / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File {filename} not found",
        )

    # Security check: ensure file is within upload directory
    try:
        file_path.resolve().relative_to(UPLOAD_DIR.resolve())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        ) from e

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )


@router.get("/list")
async def list_files():
    """
    List all uploaded files.

    Returns a list of files with their metadata.
    """
    files = []
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file():
            stat = file_path.stat()
            files.append(
                {
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "created_at": stat.st_ctime,
                    "modified_at": stat.st_mtime,
                }
            )

    return {"files": files, "total": len(files)}


@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(filename: str):
    """
    Delete a file.

    - **filename**: Name of the file to delete
    """
    file_path = UPLOAD_DIR / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File {filename} not found",
        )

    # Security check: ensure file is within upload directory
    try:
        file_path.resolve().relative_to(UPLOAD_DIR.resolve())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        ) from e

    try:
        file_path.unlink()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not delete file: {e!s}",
        ) from e
