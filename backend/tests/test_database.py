from sqlalchemy import text
from src.core.database import engine  # Updated import path
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test_database_connection():
    """Test basic database connectivity"""
    try:
        # For async engine, we need to use async methods
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1;"))
            assert result.fetchone()[0] == 1
        print("Database connection test passed!")
        return True
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False

def run_test():
    """Run the async test"""
    return asyncio.run(test_database_connection())

if __name__ == "__main__":
    run_test()