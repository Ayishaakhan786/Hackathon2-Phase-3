from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, Dict, Any
import uuid
from sqlalchemy import Column, JSON

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageBase(SQLModel):
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    role: str = Field(regex="^(user|assistant|tool)$")  # Role of the message sender ('user', 'assistant', or 'tool')
    content: str = Field(max_length=10000)  # Content of the message
    metadata_: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))  # Additional metadata about the message


class Message(MessageBase, table=True):
    """
    Represents an individual message in a conversation with content,
    sender role (user, assistant, or tool), associated conversation, and timestamp.
    """
    __tablename__ = "messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Schema for creating a new message"""
    pass


class MessageRead(MessageBase):
    """Schema for reading message data"""
    id: uuid.UUID
    timestamp: datetime