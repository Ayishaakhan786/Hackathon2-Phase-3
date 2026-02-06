from fastapi import APIRouter
from sqlalchemy import text
from datetime import datetime
import logging
from ..core.database import engine

router = APIRouter()

@router.get("/health")
async def general_health_check():
    """
    General application health check that includes database connectivity.
    """
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Check if we can connect to the database
    db_connected = False
    db_version = ""
    db_ssl_enabled = False

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            db_version = result.fetchone()[0]
            db_connected = True
            # For Neon, SSL is typically enabled by default
            db_ssl_enabled = True
    except Exception as e:
        logging.error(f"Database connection failed: {str(e)}")
        return {
            "status": "degraded",
            "timestamp": timestamp,
            "checks": {
                "database": "unhealthy",
                "api_server": "running"
            }
        }

    return {
        "status": "healthy",
        "timestamp": timestamp,
        "checks": {
            "database": "healthy",
            "api_server": "running"
        }
    }

@router.get("/health/db")
async def database_health_check():
    """
    Verify that the application can successfully connect to the Neon PostgreSQL database.
    Executes a simple query (SELECT 1) to verify connectivity.
    """
    timestamp = datetime.utcnow().isoformat() + "Z"

    try:
        # Execute a simple query to verify connectivity
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1;"))
            db_result = result.fetchone()

            if db_result and db_result[0] == 1:
                # Get database version info
                version_result = await conn.execute(text("SELECT version();"))
                db_version = version_result.fetchone()[0]

                # Log successful database connection
                logging.info("Database connection verified successfully")

                return {
                    "status": "healthy",
                    "timestamp": timestamp,
                    "database": {
                        "connected": True,
                        "version": db_version,
                        "ssl_enabled": True  # SSL is enabled via connection to Neon
                    }
                }
            else:
                raise Exception("Unexpected result from database query")
    except Exception as e:
        # Log database connection error
        logging.error(f"Database health check failed: {str(e)}")

        return {
            "status": "unhealthy",
            "timestamp": timestamp,
            "database": {
                "connected": False,
                "error": str(e),
                "details": "Unable to connect to Neon PostgreSQL database"
            }
        }