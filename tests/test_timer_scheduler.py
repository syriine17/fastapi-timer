# tests/test_scheduler.py
import uuid
from fastapi.testclient import TestClient
import pytest
import asyncio
from app.scheduler import TimerScheduler
from unittest.mock import patch
from app.main import app


client = TestClient(app)

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

def test_invalid_timer_creation():
    response = client.post("/timer", json={"hours": -1, "minutes": 0, "seconds": 0, "url": "http://testurl.com"})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_invalid_url():
    response = client.post("/timer", json={"hours": 0, "minutes": 0, "seconds": 5, "url": "invalid-url"})
    assert response.status_code == 400
    assert "detail" in response.json()

@pytest.fixture
def scheduler():
    return TimerScheduler()


@pytest.mark.asyncio
async def test_set_timer(scheduler):
    timer_id = scheduler.set_timer(0, 0, 5, "http://testurl.com")
    assert timer_id in scheduler.timers


@pytest.mark.asyncio
async def test_wait_and_trigger(scheduler):
    timer_id = scheduler.set_timer(0, 0, 1, "http://testurl.com")
    await asyncio.sleep(2)  # Wait for the timer to trigger
    assert timer_id not in scheduler.timers


@patch("httpx.AsyncClient.post")
@pytest.mark.asyncio
async def test_trigger_webhook_success(mock_post, scheduler):
    mock_post.return_value.status_code = 200
    timer_id = scheduler.set_timer(0, 0, 1, "http://testurl.com")
    await asyncio.sleep(2)  # Wait for the timer to trigger
    mock_post.assert_called_once_with("http://testurl.com", json={"id": str(timer_id)})


@patch("httpx.AsyncClient.post")
@pytest.mark.asyncio
async def test_trigger_webhook_failure(mock_post, scheduler):
    mock_post.side_effect = Exception("Network error")
    timer_id = scheduler.set_timer(0, 0, 1, "http://testurl.com")
    await asyncio.sleep(2)  # Wait for the timer to trigger
    mock_post.assert_called_once_with("http://testurl.com", json={"id": str(timer_id)})


@pytest.mark.asyncio
async def test_get_time_left(scheduler):
    timer_id = scheduler.set_timer(0, 0, 10, "http://testurl.com")
    time_left = scheduler.get_time_left(timer_id)
    assert time_left <= 10  # Ensure time left is less than or equal to 10 seconds