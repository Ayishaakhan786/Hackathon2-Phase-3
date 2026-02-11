from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from ..config.settings import settings


# Create the sync engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Set to True to see SQL queries in logs
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,  # Number of connection pools
    max_overflow=10,  # Additional connections beyond pool_size
)

# Create the session maker
SessionFactory = sessionmaker(
    bind=engine,
    expire_on_commit=False
)


def get_sync_session() -> Generator:
    """
    Dependency function that provides a sync database session.
    """
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()