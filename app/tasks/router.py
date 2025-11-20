"""Background tasks endpoints."""

import asyncio
import logging
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, EmailStr

router = APIRouter()
logger = logging.getLogger(__name__)


class EmailRequest(BaseModel):
    """Email request schema."""

    to: EmailStr
    subject: str
    body: str


class ProcessDataRequest(BaseModel):
    """Data processing request schema."""

    data: list[int]
    operation: str = "sum"


async def send_email_task(to: str, subject: str, body: str):
    """
    Simulate sending an email (background task).

    In production, this would integrate with an email service.
    """
    logger.info(f"Starting email task: {to}, {subject}")
    await asyncio.sleep(2)  # Simulate email sending delay
    logger.info(f"Email sent to {to} with subject: {subject}")


async def process_data_task(data: list[int], operation: str):
    """
    Simulate data processing (background task).

    In production, this could be a heavy computation or external API call.
    """
    logger.info(f"Starting data processing: operation={operation}, data_size={len(data)}")
    await asyncio.sleep(3)  # Simulate processing delay

    result = 0
    if operation == "sum":
        result = sum(data)
    elif operation == "avg":
        result = sum(data) / len(data) if data else 0
    elif operation == "max":
        result = max(data) if data else 0

    logger.info(f"Data processing completed: result={result}")


def write_log_task(message: str):
    """
    Write to log file (background task).

    This is a synchronous task example.
    """
    timestamp = datetime.now().isoformat()
    log_message = f"[{timestamp}] {message}\n"
    logger.info(f"Writing to log: {log_message}")


@router.post("/send-email")
async def send_email(
    email_request: EmailRequest,
    background_tasks: BackgroundTasks,
):
    """
    Send an email in the background.

    The endpoint returns immediately while the email is sent asynchronously.

    - **to**: Recipient email address
    - **subject**: Email subject
    - **body**: Email body
    """
    background_tasks.add_task(
        send_email_task,
        to=email_request.to,
        subject=email_request.subject,
        body=email_request.body,
    )

    return {
        "message": "Email task queued successfully",
        "to": email_request.to,
        "status": "processing",
    }


@router.post("/process-data")
async def process_data(
    request: ProcessDataRequest,
    background_tasks: BackgroundTasks,
):
    """
    Process data in the background.

    The endpoint returns immediately while data is processed asynchronously.

    - **data**: List of integers to process
    - **operation**: Operation to perform (sum, avg, max)
    """
    background_tasks.add_task(
        process_data_task,
        data=request.data,
        operation=request.operation,
    )

    return {
        "message": "Data processing task queued successfully",
        "operation": request.operation,
        "data_size": len(request.data),
        "status": "processing",
    }


@router.post("/log")
async def create_log(
    message: str,
    background_tasks: BackgroundTasks,
):
    """
    Create a log entry in the background.

    - **message**: Message to log
    """
    background_tasks.add_task(write_log_task, message=message)

    return {
        "message": "Log task queued successfully",
        "status": "processing",
    }


@router.post("/multiple-tasks")
async def multiple_tasks(
    background_tasks: BackgroundTasks,
):
    """
    Demonstrate multiple background tasks.

    Queues multiple tasks that will run asynchronously.
    """
    # Add multiple tasks
    background_tasks.add_task(write_log_task, "Task 1: Started")
    background_tasks.add_task(write_log_task, "Task 2: Started")
    background_tasks.add_task(
        send_email_task,
        to="admin@example.com",
        subject="Multiple Tasks Test",
        body="This is a test of multiple background tasks",
    )
    background_tasks.add_task(process_data_task, data=[1, 2, 3, 4, 5], operation="sum")

    return {
        "message": "Multiple tasks queued successfully",
        "tasks_count": 4,
        "status": "processing",
    }
