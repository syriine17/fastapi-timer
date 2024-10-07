import time
import uuid
import asyncio
import httpx
import logging

class TimerScheduler:
    """
    A scheduler for managing timers and triggering webhooks upon expiration.
    
    Attributes:
        timers (dict): A dictionary to store timers with their expiration time and associated URL.
    """

    def __init__(self):
        """Initialize the TimerScheduler with an empty timers dictionary and set logging level."""
        self.timers = {}
        logging.basicConfig(level=logging.INFO)

    def set_timer(self, hours: int, minutes: int, seconds: int, url: str) -> uuid.UUID:
        """
        Set a timer with the specified duration and URL.
        
        Args:
            hours (int): The number of hours for the timer.
            minutes (int): The number of minutes for the timer.
            seconds (int): The number of seconds for the timer.
            url (str): The URL to trigger when the timer expires.
        
        Returns:
            uuid.UUID: The unique ID of the created timer.
        """
        timer_id = uuid.uuid4()
        expiration_time = time.time() + (hours * 3600 + minutes * 60 + seconds)
        self.timers[timer_id] = (expiration_time, url)
        asyncio.create_task(self._wait_and_trigger(timer_id, expiration_time, url))
        return timer_id

    async def _wait_and_trigger(self, timer_id: uuid.UUID, expiration_time: float, url: str):
        """
        Wait until the timer expires and then trigger the associated webhook.
        
        Args:
            timer_id (uuid.UUID): The unique ID of the timer.
            expiration_time (float): The expiration time of the timer.
            url (str): The URL to trigger when the timer expires.
        """
        await asyncio.sleep(max(0, expiration_time - time.time()))
        await self.trigger_webhook(timer_id, url)
        # Remove the timer from the dictionary after it's triggered
        if timer_id in self.timers:
            del self.timers[timer_id]

    async def trigger_webhook(self, timer_id: uuid.UUID, url: str):
        """
        Trigger the webhook associated with the timer.
        
        Args:
            timer_id (uuid.UUID): The unique ID of the timer.
            url (str): The URL to trigger.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json={"id": str(timer_id)})
                logging.info(f"Webhook triggered for {timer_id}, response: {response.status_code}")
            except Exception as e:
                logging.error(f"Failed to trigger webhook for {timer_id}: {e}")

    def get_time_left(self, timer_id: uuid.UUID) -> float:
        """
        Get the time left for the specified timer.
        
        Args:
            timer_id (uuid.UUID): The unique ID of the timer.
        
        Returns:
            float: The time left in seconds, or -1 if the timer does not exist.
        """
        expiration_time, _ = self.timers.get(timer_id, (None, None))
        if expiration_time is None:
            return -1
        return max(0, expiration_time - time.time())

    async def trigger_expired_timers(self):
        """
        Check for expired timers and trigger their associated webhooks.
        """
        current_time = time.time()
        expired_timers = [timer_id for timer_id, (expiration_time, _) in self.timers.items() if expiration_time <= current_time]
        # for timer_id, (expiration_time, url) in list(self.timers.items()):
        for timer_id in expired_timers:
            expiration_time, url = self.timers[timer_id]
            await self.trigger_webhook(timer_id, url)
            del self.timers[timer_id]
