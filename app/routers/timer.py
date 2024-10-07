import time
import uuid
import validators
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import TimerCreate, TimerResponse, TimerStatusResponse
from app.database import get_db
from app.models import Timer
from app.scheduler import TimerScheduler

router = APIRouter()
scheduler = TimerScheduler()

@router.post("/timer", response_model=TimerResponse)
async def set_timer(
    timer: TimerCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Set a timer with the specified duration and URL.

    Args:
        timer (TimerCreate): The timer details containing the URL and duration.
        db (AsyncSession): The database session.

    Raises:
        HTTPException: If the timer values are invalid or the URL format is incorrect.

    Returns:
        TimerResponse: The created timer's ID and time left.
    """
    print(f"Received: url={timer.url}, hours={timer.hours}, minutes={timer.minutes}, seconds={timer.seconds}")
    
    # Validate timer values
    if timer.hours < 0 or timer.minutes < 0 or timer.seconds < 0:
        raise HTTPException(status_code=400, detail="Invalid timer values")
    
    # Validate URL
    if not validators.url(timer.url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    async with db.begin():
        timer_id = uuid.uuid4()  # Generate the UUID here
        new_timer = Timer(
            id=timer_id,
            url=timer.url,
            hours=timer.hours,
            minutes=timer.minutes,
            seconds=timer.seconds
        )
        db.add(new_timer)

    await db.commit()
    await db.refresh(new_timer)  # Refresh the new_timer after commit

    time_left = timer.hours * 3600 + timer.minutes * 60 + timer.seconds
    scheduler.set_timer(timer.hours, timer.minutes, timer.seconds, timer.url)  # Set the timer
    return TimerResponse(id=timer_id, time_left=time_left)

@router.get("/timer/{timer_id}", response_model=TimerStatusResponse)
async def get_timer(
    timer_id: UUID, 
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve the status of a timer by its ID.

    Args:
        timer_id (UUID): The ID of the timer.
        db (AsyncSession): The database session.

    Raises:
        HTTPException: If the timer is not found.

    Returns:
        TimerStatusResponse: The timer's ID and time left.
    """
    timer = await db.get(Timer, timer_id)  # Use await db.get for async retrieval
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")

    total_duration = timer.hours * 3600 + timer.minutes * 60 + timer.seconds
    current_time = time.time()
    creation_time = timer.creation_time.timestamp()  # Convert to timestamp
    time_left = max(0, total_duration - (current_time - creation_time))

    return TimerStatusResponse(id=timer_id, time_left=time_left)
