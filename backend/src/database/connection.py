from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
from ..config.settings import DATABASE_URL
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.task import Task  # Import Task model
import logging

# Create the SQLModel engine with connection pooling and SSL configuration
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # Number of connections to maintain in the pool
    max_overflow=10,  # Additional connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections after 5 minutes
    pool_timeout=30,  # Time to wait before giving up on getting a connection
    echo=False  # Enable SQL query logging based on DEBUG setting
)

def get_session() -> Session:
    """
    Dependency function to get database session
    """
    with Session(engine) as session:
        yield session

# Log successful database connection
logging.info("Database engine created successfully with SSL configuration")

def get_connection_stats():
    """
    Get connection pool statistics
    """
    pool = engine.pool
    return {
        "checked_out": pool.checkedout(),
        "size": pool.size(),
        "overflow": pool.overflow(),
        "connections_active": getattr(engine, "pool")._checkedout(),
    }

def create_db_and_tables():
    """
    Create database tables if they don't exist
    """
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    logging.info("Database tables created successfully")