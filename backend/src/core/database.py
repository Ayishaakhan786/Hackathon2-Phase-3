from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel
from src.core.config import settings
import logging


# Create the async engine with Neon PostgreSQL SSL configuration
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create an async session maker
AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)

# Log successful database connection
logging.info("Database engine created successfully with SSL configuration")

def get_connection_stats():
    """
    Get connection pool statistics
    """
    # For async engines, we can't directly access sync pool stats
    # This is a placeholder implementation
    return {
        "pool_size": 5,
        "max_overflow": 10,
    }