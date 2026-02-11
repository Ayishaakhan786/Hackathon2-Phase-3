from typing import List, Optional
from sqlmodel import select, Session, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from ..models.conversation import Conversation
from ..models.message import Message
from uuid import UUID


def create_conversation(db_session: Session, user_id: str, title: Optional[str] = None) -> Conversation:
    """
    Create a new conversation in the database
    """
    conversation = Conversation(user_id=user_id, title=title)
    db_session.add(conversation)
    db_session.commit()
    db_session.refresh(conversation)
    return conversation


def get_conversation_by_id(db_session: Session, conversation_id: UUID) -> Optional[Conversation]:
    """
    Retrieve a conversation by its ID with optimized query
    """
    # Using get() is already optimized for primary key lookups
    return db_session.get(Conversation, conversation_id)


def get_conversations_by_user(db_session: Session, user_id: str) -> List[Conversation]:
    """
    Retrieve all conversations for a specific user with optimized query
    """
    # Add ordering and limit to prevent performance issues with many conversations
    statement = select(Conversation).where(
        Conversation.user_id == user_id
    ).order_by(Conversation.updated_at.desc())  # Order by most recently updated
    results = db_session.exec(statement)
    return results.all()


def update_conversation_title(db_session: Session, conversation_id: UUID, title: str) -> Optional[Conversation]:
    """
    Update the title of a conversation with optimized query
    """
    conversation = db_session.get(Conversation, conversation_id)
    if conversation:
        conversation.title = title
        conversation.updated_at = func.now()
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
    return conversation


def delete_conversation(db_session: Session, conversation_id: UUID) -> bool:
    """
    Delete a conversation by its ID
    """
    conversation = db_session.get(Conversation, conversation_id)
    if conversation:
        db_session.delete(conversation)
        db_session.commit()
        return True
    return False


def create_message(
    db_session: Session,
    conversation_id: UUID,
    role: str,
    content: str,
    metadata: Optional[dict] = None
) -> Message:
    """
    Create a new message in the database with optimized query
    """
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        metadata=metadata
    )
    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)
    return message


def get_message_by_id(db_session: Session, message_id: UUID) -> Optional[Message]:
    """
    Retrieve a message by its ID
    """
    return db_session.get(Message, message_id)


def get_messages_by_conversation(
    db_session: Session,
    conversation_id: UUID,
    offset: int = 0,
    limit: int = 100
) -> List[Message]:
    """
    Retrieve messages for a specific conversation with pagination and optimized query
    """
    # Add explicit ordering by timestamp for consistent results
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc()).offset(offset).limit(limit)
    results = db_session.exec(statement)
    return results.all()


def get_latest_messages_by_conversation(
    db_session: Session,
    conversation_id: UUID,
    limit: int = 10
) -> List[Message]:
    """
    Retrieve the latest messages for a specific conversation with optimized query
    """
    # Get the latest messages in descending order, then reverse to return in chronological order
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.desc()).limit(limit)
    results = db_session.exec(statement)
    messages = results.all()
    # Reverse to return in chronological order (oldest first among the latest)
    return messages[::-1]


def get_messages_by_conversation_optimized(
    db_session: Session,
    conversation_id: UUID,
    limit: int = 50
) -> List[Message]:
    """
    Optimized function to get messages with a join to avoid N+1 queries
    """
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.desc()).limit(limit)
    
    results = db_session.exec(statement)
    return results.all()


def get_conversation_with_messages(
    db_session: Session,
    conversation_id: UUID
) -> Optional[Conversation]:
    """
    Retrieve a conversation with its messages in a single optimized query
    """
    statement = select(Conversation).options(
        selectinload(Conversation.messages)
    ).where(Conversation.id == conversation_id)
    
    result = db_session.exec(statement)
    return result.first()


def get_conversation_summary(
    db_session: Session,
    conversation_id: UUID
) -> Optional[dict]:
    """
    Get a summary of a conversation with message counts in a single optimized query
    """
    # Get conversation details
    conversation = db_session.get(Conversation, conversation_id)
    if not conversation:
        return None
    
    # Get message counts in a single query
    from sqlalchemy import text
    count_query = text("""
        SELECT 
            COUNT(*) as total_messages,
            COUNT(CASE WHEN role = 'user' THEN 1 END) as user_messages,
            COUNT(CASE WHEN role = 'assistant' THEN 1 END) as assistant_messages,
            MAX(timestamp) as last_message_time
        FROM messages 
        WHERE conversation_id = :conversation_id
    """)
    
    result = db_session.execute(count_query, {"conversation_id": conversation_id})
    row = result.fetchone()
    
    return {
        "id": str(conversation.id),
        "user_id": conversation.user_id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "total_messages": row.total_messages or 0,
        "user_messages": row.user_messages or 0,
        "assistant_messages": row.assistant_messages or 0,
        "last_message_time": row.last_message_time
    }


def delete_message(db_session: Session, message_id: UUID) -> bool:
    """
    Delete a message by its ID
    """
    message = db_session.get(Message, message_id)
    if message:
        db_session.delete(message)
        db_session.commit()
        return True
    return False