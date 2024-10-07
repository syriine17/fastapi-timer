from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://myuser:mysecretpassword@db/mydatabase"


# Create the async engine and session
async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

# Dependency to get the async session
async def get_db() -> AsyncSession:
    """
    Provides a database session for dependency injection.

    Yields:
        AsyncSession: A session to interact with the database.
    """
    async with AsyncSessionLocal() as session:
        yield session
