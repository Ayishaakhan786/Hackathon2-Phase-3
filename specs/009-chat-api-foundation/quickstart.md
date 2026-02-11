# Quickstart Guide: Chat API Foundation

## Overview
This guide explains how to set up and use the chat API foundation for conversation persistence and message handling.

## Prerequisites
- Python 3.9+
- Poetry (dependency manager)
- Neon PostgreSQL database instance

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy the environment template
cp .env.example .env

# Update the database connection string in .env
DATABASE_URL="postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname"
```

### 2. Install Dependencies
```bash
poetry install
poetry shell
```

### 3. Initialize Database Tables
```bash
# Run the database initialization script
python -m src.db.init_tables
```

## API Usage

### Starting a New Conversation
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how can you help me?"
  }'
```

### Continuing an Existing Conversation
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv456",
    "message": "Tell me more about this."
  }'
```

## Expected Response Format
```json
{
  "conversation_id": "string",
  "response": "string",
  "tool_calls": []
}
```

## Key Components

### Models
- `Conversation`: Manages conversation metadata
- `Message`: Stores individual messages with roles and timestamps

### Services
- `create_conversation(user_id)`: Creates a new conversation
- `get_conversation(conversation_id, user_id)`: Retrieves a specific conversation
- `save_message(user_id, conversation_id, role, content)`: Persists a message
- `fetch_conversation_history(conversation_id)`: Gets all messages in a conversation

### API Endpoint
- `POST /api/{user_id}/chat`: Main entry point for chat interactions