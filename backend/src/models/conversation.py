from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List, Dict, Any
import uuid
from sqlalchemy import Column, DateTime, JSON

if TYPE_CHECKING:
    from .message import Message


class ConversationBase(SQLModel):
    user_id: str
    title: Optional[str] = None
    metadata_: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP", "onupdate": "CURRENT_TIMESTAMP"})

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationRead(ConversationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    messages: List["Message"] = []