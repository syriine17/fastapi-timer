import pytest
from fastapi import HTTPException
from app.scheduler import TimerScheduler

@pytest.fixture
def scheduler():
    return TimerScheduler()

@pytest.mark.asyncio
async def test_invalid_url(scheduler):
    with pytest.raises(HTTPException):
        scheduler.set_timer(0, 0, 5, "invalid-url")

@pytest.mark.asyncio
async def test_negative_timer_values(scheduler):
    with pytest.raises(HTTPException):
        scheduler.set_timer(-1, 0, 0, "http://testurl.com")
