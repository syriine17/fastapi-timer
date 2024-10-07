from fastapi import FastAPI
from app.routers.timer import router as timer_router
from app.database import async_engine
from app.models import Base
from contextlib import asynccontextmanager
from app.scheduler import TimerScheduler

scheduler = TimerScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the lifespan of the FastAPI application.
    This function creates the database tables and triggers expired timers
    upon application shutdown.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await scheduler.trigger_expired_timers()

app = FastAPI(lifespan=lifespan)

# Include the timer router
app.include_router(timer_router)
