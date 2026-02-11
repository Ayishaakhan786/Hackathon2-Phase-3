"""
Integration test for new conversation creation
This test verifies that the full flow of creating a new conversation works correctly
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.connection import create_db_and_tables, engine
from sqlmodel import SQLModel, Session
from unittest.mock import patch
from src.models.conversation import Conversation
from src.models.message import Message


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        # Create tables for testing
        SQLModel.metadata.create_all(bind=engine)
        yield test_client
        # Clean up after test
        SQLModel.metadata.drop_all(bind=engine)


def test_create_new_conversation_integration(client):
    """Test the full flow of creating a new conversation"""
    user_id = "test_user_123"
    
    # Mock the placeholder response to have predictable output
    mock_assistant_response = "This is a mocked assistant response for testing."
    
    with patch('src.api.chat_api.chat', side_effect=lambda user_id, chat_request, session: type(
        'MockResponse', (), {
            'conversation_id': 'mock_conversation_id',
            'response': mock_assistant_response,
            'tool_calls': []
        })()):
        
        # Send a request to create a new conversation (no conversation_id provided)
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Hello, start a new conversation!"}
        )
        
        # Verify the response
        assert response.status_code == 200
        response_data = response.json()
        
        # Check that a conversation ID was returned
        assert "conversation_id" in response_data
        assert response_data["conversation_id"] != ""
        
        # Check that a response was provided
        assert "response" in response_data
        assert response_data["response"] == mock_assistant_response
        
        # Check that tool_calls is an empty list
        assert response_data["tool_calls"] == []


def test_new_conversation_persists_in_database(client):
    """Test that new conversations and messages are properly persisted in the database"""
    user_id = "test_user_456"
    test_message = "This is a test message for integration."
    
    # Send a request to create a new conversation
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": test_message}
    )
    
    # Verify the response
    assert response.status_code == 200
    response_data = response.json()
    
    conversation_id = response_data["conversation_id"]
    assert conversation_id != ""
    
    # Verify that the conversation and messages were saved to the database
    # We'll need to access the database directly to verify persistence
    from src.database.connection import engine
    from sqlmodel import select
    
    with Session(engine) as session:
        # Check that the conversation exists
        conversation_statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = session.exec(conversation_statement).first()
        assert conversation is not None
        assert conversation.user_id == user_id
        
        # Check that the user's message was saved
        user_message_statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.role == "user",
            Message.content == test_message
        )
        user_message = session.exec(user_message_statement).first()
        assert user_message is not None
        assert user_message.user_id == user_id
        
        # Check that the assistant's response was saved
        assistant_message_statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.role == "assistant"
        )
        assistant_messages = session.exec(assistant_message_statement).all()
        # There should be at least one assistant message
        assert len(assistant_messages) >= 1