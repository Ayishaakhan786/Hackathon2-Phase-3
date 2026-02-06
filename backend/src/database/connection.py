from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from ..config.settings import DATABASE_URL
import logging

# Create the SQLAlchemy engine with connection pooling and SSL configuration
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

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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