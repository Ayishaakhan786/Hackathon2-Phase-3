from typing import List, Optional
from sqlmodel import select, Session, func
from sqlalchemy.exc import IntegrityError
from ..models.conversation import Conversation, Message
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
    Retrieve a conversation by its ID
    """
    return db_session.get(Conversation, conversation_id)


def get_conversations_by_user(db_session: Session, user_id: str) -> List[Conversation]:
    """
    Retrieve all conversations for a specific user
    """
    statement = select(Conversation).where(Conversation.user_id == user_id)
    results = db_session.exec(statement)
    return results.all()


def update_conversation_title(db_session: Session, conversation_id: UUID, title: str) -> Optional[Conversation]:
    """
    Update the title of a conversation
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
    Create a new message in the database
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
    Retrieve messages for a specific conversation with pagination
    """
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp).offset(offset).limit(limit)
    results = db_session.exec(statement)
    return results.all()


def get_latest_messages_by_conversation(
    db_session: Session, 
    conversation_id: UUID, 
    limit: int = 10
) -> List[Message]:
    """
    Retrieve the latest messages for a specific conversation
    """
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.desc()).limit(limit)
    results = db_session.exec(statement)
    # Return in chronological order (oldest first)
    return results.all()[::-1]


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