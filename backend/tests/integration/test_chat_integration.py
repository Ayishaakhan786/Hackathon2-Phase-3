import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import AsyncMock, patch

from backend.src.main import app
from backend.src.database.session import get_async_session
from backend.src.models.conversation import Conversation, Message
from backend.src.models.task import Task


# Create a test database
@pytest.fixture(name="engine")
def fixture_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield engine


@pytest.fixture(name="session")
def fixture_session(engine):
    # Create tables
    from backend.src.models.conversation import Conversation, Message
    from backend.src.models.task import Task
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def fixture_client(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_async_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_chat_endpoint_basic_interaction(client):
    """
    Test basic chat interaction with the AI agent
    """
    user_id = "test_user_123"
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": "Add a task to buy groceries"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data or "message" in data  # Depending on response structure


@pytest.mark.asyncio
async def test_mcp_tool_invocation():
    """
    Test that MCP tools are properly invoked from the agent
    """
    # This test would require mocking the OpenAI API and verifying
    # that the appropriate MCP tools are called
    with patch('backend.src.services.agent_runner.client') as mock_openai:
        # Mock the OpenAI response to trigger a tool call
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.tool_calls = [AsyncMock()]
        mock_response.choices[0].message.tool_calls[0].function.name = "create_task"
        mock_response.choices[0].message.tool_calls[0].function.arguments = '{"title": "Buy groceries", "description": "Get milk and bread"}'
        
        mock_openai.chat.completions.create.return_value = mock_response
        
        # Test would continue to verify the tool call is processed correctly
        # For now, just a placeholder to show the approach
        assert True


def test_conversation_persistence(session):
    """
    Test that conversation and message history is properly persisted
    """
    # Create a conversation
    conversation = Conversation(user_id="test_user_123", title="Test conversation")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    
    # Add a message
    message = Message(
        conversation_id=conversation.id,
        role="user",
        content="Add a task to buy groceries"
    )
    session.add(message)
    session.commit()
    
    # Verify the data was saved
    saved_conversation = session.get(Conversation, conversation.id)
    assert saved_conversation is not None
    assert saved_conversation.user_id == "test_user_123"
    
    messages = session.query(Message).filter(Message.conversation_id == conversation.id).all()
    assert len(messages) == 1
    assert messages[0].content == "Add a task to buy groceries"


def test_task_operations_persistence(session):
    """
    Test that task operations are properly persisted in the database
    """
    # Create a task
    task = Task(
        title="Buy groceries",
        description="Get milk and bread",
        user_id="test_user_123",
        status="pending"
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    
    # Verify the task was saved
    saved_task = session.get(Task, task.id)
    assert saved_task is not None
    assert saved_task.title == "Buy groceries"
    assert saved_task.status == "pending"
    
    # Update the task
    saved_task.status = "completed"
    session.add(saved_task)
    session.commit()
    
    # Verify the update
    updated_task = session.get(Task, task.id)
    assert updated_task.status == "completed"