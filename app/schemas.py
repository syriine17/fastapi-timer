from pydantic import BaseModel
from uuid import UUID

class TimerCreate(BaseModel):
    """
    Represents the request schema for creating a timer.

    Attributes:
        url (str): The URL to trigger when the timer expires.
        hours (int): The duration in hours.
        minutes (int): The duration in minutes.
        seconds (int): The duration in seconds.
    """
    url: str
    hours: int
    minutes: int
    seconds: int

class TimerResponse(BaseModel):
    """
    Represents the response schema for setting a timer.

    Attributes:
        id (UUID): The unique identifier for the timer.
        time_left (int): The amount of seconds left until the timer expires.
    """
    id: UUID
    time_left: int

class TimerStatusResponse(BaseModel):
    """
    Represents the response schema for retrieving a timer's status.

    Attributes:
        id (UUID): The unique identifier for the timer.
        time_left (int): The amount of seconds left until the timer expires.
    """
    id: UUID
    time_left: int
