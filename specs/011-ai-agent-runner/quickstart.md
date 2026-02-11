# Quickstart Guide: AI Agent, Runner & Stateless Chat Orchestration

## Overview
This guide provides a quick introduction to implementing the AI-powered conversational agent system that enables natural language task management using OpenAI Agents SDK, MCP tools, and Neon PostgreSQL database.

## Prerequisites
- Python 3.11+
- Poetry (dependency management)
- Access to OpenAI API
- Access to Neon PostgreSQL database
- MCP server with task tools

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies
```bash
cd backend
poetry install
poetry shell
```

### 3. Environment Configuration
Create a `.env` file in the backend directory with the following variables:
```env
OPENAI_API_KEY=<your-openai-api-key>
DATABASE_URL=<your-neon-postgres-connection-string>
MCP_SERVER_URL=<your-mcp-server-url>
MCP_API_KEY=<your-mcp-api-key>
```

### 4. Database Setup
Run the database migrations:
```bash
poetry run alembic upgrade head
```

## Key Components

### 1. Conversation and Message Models
Located in `src/models/conversation.py`, these models define the data structures for storing conversation history:

```python
class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str
    title: Optional[str] = None
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())
    
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    role: str = Field(regex="^(user|assistant|tool)$")
    content: str = Field(max_length=10000)
    timestamp: datetime = Field(default=datetime.utcnow())
    
    conversation: Conversation = Relationship(back_populates="messages")
```

### 2. AI Agent Runner
The agent runner orchestrates the interaction between the API, database, and AI agent:

```python
class AgentRunner:
    def __init__(self, db_session: AsyncSession, openai_client: OpenAI):
        self.db_session = db_session
        self.openai_client = openai_client
    
    async def run_agent(self, user_id: str, message: str, conversation_id: Optional[uuid.UUID] = None):
        # 1. Retrieve conversation context from DB
        conversation = await self.get_or_create_conversation(user_id, conversation_id)
        
        # 2. Build message history from DB
        messages = await self.get_conversation_messages(conversation.id)
        
        # 3. Invoke AI agent with context and tools
        response = await self.invoke_agent(messages, user_message=message)
        
        # 4. Persist new messages to DB
        await self.save_messages(conversation.id, [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response}
        ])
        
        return {"conversation_id": conversation.id, "response": response}
```

### 3. API Endpoint
The stateless chat endpoint handles user requests:

```python
@router.post("/api/{user_id}/chat")
async def chat_with_agent(
    user_id: str,
    request: ChatRequest,
    db_session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    # Verify user authorization
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Run the agent and return response
    agent_runner = AgentRunner(db_session, openai_client)
    result = await agent_runner.run_agent(
        user_id=user_id,
        message=request.message,
        conversation_id=request.conversation_id
    )
    
    return result
```

## Running the Application

### 1. Start the Backend Server
```bash
cd backend
poetry run uvicorn src.main:app --reload --port 8000
```

### 2. Verify the Setup
Send a test request to the chat endpoint:
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

## Key Architecture Points

1. **Stateless Design**: Each API request fetches the conversation context from the database, ensuring no in-memory state is maintained between requests.

2. **MCP Tool Integration**: The AI agent is configured with MCP tools that handle all task operations, preventing direct database access from the agent.

3. **Database Persistence**: All user messages and AI responses are stored in the database, ensuring conversation continuity across server restarts.

4. **Separation of Concerns**: Clear separation between FastAPI (HTTP layer), OpenAI Agents SDK (reasoning), and MCP tools (task operations).

## Troubleshooting

### Common Issues

1. **OpenAI API Connection Errors**:
   - Verify your `OPENAI_API_KEY` is set correctly
   - Check your internet connection and firewall settings

2. **Database Connection Issues**:
   - Ensure your `DATABASE_URL` is configured correctly
   - Verify the database migration has been run

3. **MCP Tool Invocation Failures**:
   - Confirm the MCP server is running and accessible
   - Check that the required tools are registered with the MCP server

### Logging
Enable debug logging by setting the environment variable:
```bash
export LOG_LEVEL=DEBUG
```

## Next Steps

1. Integrate with the frontend chat interface
2. Implement additional MCP tools for advanced task operations
3. Add analytics and usage tracking
4. Enhance error handling and user feedback mechanisms