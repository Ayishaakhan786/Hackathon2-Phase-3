from typing import List
from sqlmodel import select, Session
from ..models.message import Message, MessageCreate
from datetime import datetime
import uuid


def save_message(*, session: Session, conversation_id: uuid.UUID, role: str, content: str) -> Message:
    """
    Save a message to the database.

    Args:
        session: Database session
        conversation_id: ID of the conversation the message belongs to
        role: Role of the sender ('user', 'assistant', or 'tool')
        content: Content of the message

    Returns:
        The saved Message object
    """
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def fetch_conversation_history(*, session: Session, conversation_id: uuid.UUID) -> List[Message]:
    """
    Fetch all messages in a conversation, ordered by creation time.

    Args:
        session: Database session
        conversation_id: ID of the conversation to fetch history for

    Returns:
        List of Message objects in chronological order
    """
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc())
    messages = session.exec(statement).all()
    return messages


def fetch_formatted_conversation_history(*, session: Session, conversation_id: uuid.UUID) -> List[dict]:
    """
    Fetch all messages in a conversation formatted for API response, ordered by creation time.

    Args:
        session: Database session
        conversation_id: ID of the conversation to fetch history for

    Returns:
        List of message dictionaries in chronological order
    """
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc())
    messages = session.exec(statement).all()

    # Format messages as dictionaries
    formatted_messages = []
    for message in messages:
        formatted_messages.append({
            "id": str(message.id),
            "conversation_id": str(message.conversation_id),
            "role": message.role,
            "content": message.content,
            "timestamp": message.timestamp.isoformat() if message.timestamp else None
        })

    return formatted_messages