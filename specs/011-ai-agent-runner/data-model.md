# Data Model: AI Agent, Runner & Stateless Chat Orchestration

## Overview
This document defines the data models for the AI-powered conversational agent system, including entities for conversations, messages, and their relationships.

## Entity Definitions

### Conversation
Represents a chat session with unique identifier, associated user, and timestamps for creation and last update.

**Fields:**
- `id` (UUID, Primary Key): Unique identifier for the conversation
- `user_id` (String): Identifier of the user who owns this conversation
- `title` (String, Optional): Auto-generated title based on the first message or topic
- `created_at` (DateTime): Timestamp when the conversation was created
- `updated_at` (DateTime): Timestamp when the conversation was last updated
- `metadata` (JSON, Optional): Additional metadata about the conversation

**Validation Rules:**
- `user_id` is required and must correspond to a valid user
- `created_at` defaults to current timestamp
- `updated_at` updates automatically on any change

**Relationships:**
- One-to-Many: A conversation has many messages

### Message
Represents an individual message in a conversation with content, sender role (user/assistant), associated conversation, and timestamp.

**Fields:**
- `id` (UUID, Primary Key): Unique identifier for the message
- `conversation_id` (UUID, Foreign Key): Reference to the parent conversation
- `role` (String): Role of the message sender ('user', 'assistant', or 'tool')
- `content` (Text): The content of the message
- `timestamp` (DateTime): When the message was created
- `metadata` (JSON, Optional): Additional metadata about the message (e.g., tool call details)

**Validation Rules:**
- `conversation_id` is required and must reference an existing conversation
- `role` must be one of 'user', 'assistant', or 'tool'
- `content` is required and must not exceed 10,000 characters
- `timestamp` defaults to current timestamp

**Relationships:**
- Many-to-One: A message belongs to one conversation

## State Transitions

### Conversation States
- `active`: The conversation is currently in progress
- `archived`: The conversation has been archived by the user
- `deleted`: The conversation has been marked for deletion (soft delete)

### Message States
- `pending`: The message has been received but not yet processed
- `processed`: The message has been processed by the AI agent
- `error`: An error occurred during processing

## Database Schema

```sql
-- Conversation table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- Index for efficient user conversation lookup
CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Message table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'tool')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- Index for efficient conversation message lookup
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
-- Index for chronological message ordering
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
```

## SQLModel Implementation

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid

class ConversationBase(SQLModel):
    user_id: str
    title: Optional[str] = None
    metadata: Optional[dict] = None

class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())
    
    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")

class MessageBase(SQLModel):
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    role: str = Field(regex="^(user|assistant|tool)$")
    content: str = Field(max_length=10000)
    metadata: Optional[dict] = None

class Message(MessageBase, table=True):
    __tablename__ = "messages"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime = Field(default=datetime.utcnow())
    
    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")
```

## API Representation

### Conversation Resource
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "user_id": "user123",
  "title": "Grocery list management",
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T14:30:00Z",
  "metadata": {}
}
```

### Message Resource
```json
{
  "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
  "conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "role": "user",
  "content": "Add milk to my grocery list",
  "timestamp": "2023-10-01T12:05:00Z",
  "metadata": {}
}
```

## Data Flow

1. **New Conversation Creation**: When a user starts a new conversation, a Conversation record is created with the user_id and an auto-generated title based on the first message.

2. **Message Addition**: Each user message and AI response is stored as a Message record linked to the conversation.

3. **Context Retrieval**: For each AI agent run, the system retrieves the conversation and its messages ordered by timestamp to provide context.

4. **State Management**: Messages transition from 'pending' to 'processed' as they're handled by the AI agent.

## Validation Rules

- All user inputs must be sanitized to prevent injection attacks
- Conversation access is restricted to the owning user
- Message content is validated for length and appropriate content
- Foreign key constraints ensure referential integrity