from sqlmodel import SQLModel
from typing import List
import asyncio
from .database.session import engine


async def create_db_and_tables():
    """
    Creates the database and all tables defined in the SQLModel models.
    This function should be called on application startup.
    """
    async with engine.begin() as conn:
        # Create all tables defined in SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)


def get_model_list() -> List[type]:
    """
    Returns a list of all SQLModel model classes.
    Useful for Alembic migrations and other meta operations.
    """
    # This will be populated with actual models as they are defined
    from .models.conversation import Conversation, Message
    return [Conversation, Message]