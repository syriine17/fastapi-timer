# tests/test_scheduler.py
import uuid
import pytest
import asyncio
from app.scheduler import TimerScheduler
from unittest.mock import patch

@pytest.mark.asyncio
async def test_set_timer():
    """
    Test that a timer is set correctly and returns a valid UUID.
    """
    scheduler = TimerScheduler()
    timer_id = scheduler.set_timer(0, 0, 5, "http://example.com")
    
    assert timer_id is not None
    assert isinstance(timer_id, uuid.UUID)

@pytest.mark.asyncio
async def test_get_time_left():
    """
    Test the time left for a timer.
    """
    scheduler = TimerScheduler()
    timer_id = scheduler.set_timer(0, 0, 5, "http://example.com")
    
    # Get the time left immediately
    time_left = scheduler.get_time_left(timer_id)
    assert 0 <= time_left <= 5  # Since it's set for 5 seconds

@pytest.mark.asyncio
@patch("app.scheduler.httpx.AsyncClient.post")
async def test_trigger_webhook(mock_post):
    """
    Test that the webhook is triggered with the correct data.
    """
    scheduler = TimerScheduler()
    timer_id = uuid.uuid4()

    # Mock the httpx post method to avoid actual network calls
    mock_post.return_value.status_code = 200

    await scheduler.trigger_webhook(timer_id, "http://example.com")
    
    # Ensure that the mock_post was called with the expected arguments
    mock_post.assert_called_once_with("http://example.com", json={"id": str(timer_id)})

@pytest.mark.asyncio
async def test_timer_expiration():
    """
    Test that a timer is triggered and removed from the timers dictionary after expiration.
    """
    scheduler = TimerScheduler()

    # Set a short timer for 1 second
    timer_id = scheduler.set_timer(0, 0, 1, "http://example.com")
    
    # Ensure the timer is present in the scheduler
    assert timer_id in scheduler.timers
    
    # Wait for the timer to expire
    await asyncio.sleep(1.5)
    
    # Check that the timer is no longer in the scheduler
    assert timer_id not in scheduler.timers

@pytest.mark.asyncio
@patch("app.scheduler.TimerScheduler.trigger_webhook")
async def test_trigger_expired_timers(mock_trigger_webhook):
    """
    Test that expired timers are correctly triggered by trigger_expired_timers.
    """
    scheduler = TimerScheduler()

    # Set two timers, one for 1 second and one for 5 seconds
    timer_id_1 = scheduler.set_timer(0, 0, 1, "http://example.com/1")
    timer_id_2 = scheduler.set_timer(0, 0, 5, "http://example.com/2")
    
    # Wait for the first timer to expire
    await asyncio.sleep(1.5)
    
    # Call trigger_expired_timers to manually trigger any expired timers
    await scheduler.trigger_expired_timers()
    
    # Ensure that the webhook was triggered for the first timer, but not the second
    mock_trigger_webhook.assert_called_once_with(timer_id_1, "http://example.com/1")
    assert timer_id_1 not in scheduler.timers
    assert timer_id_2 in scheduler.timers
