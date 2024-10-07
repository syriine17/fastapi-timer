from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Timer(Base):
    """
    Represents a timer in the database.

    Attributes:
        id (UUID): The unique identifier for the timer.
        url (str): The URL to trigger when the timer expires.
        hours (int): The duration in hours.
        minutes (int): The duration in minutes.
        seconds (int): The duration in seconds.
        expiration_time (float): The time at which the timer expires.
        creation_time (datetime): The time the timer was created.
    """
    __tablename__ = "timers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    url = Column(String)
    hours = Column(Integer)
    minutes = Column(Integer)
    seconds = Column(Integer)
    expiration_time = Column(Float)
    creation_time = Column(DateTime, default=datetime.utcnow)
