"""
Integration test for continuing existing conversation functionality
This test verifies that the full flow of continuing an existing conversation works correctly
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.connection import create_db_and_tables, engine
from sqlmodel import SQLModel, Session, select
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


def test_continue_existing_conversation_integration(client):
    """Test the full flow of continuing an existing conversation"""
    user_id = "test_user_123"
    
    # First, create a conversation by making an initial request
    initial_message = "Hello, start a new conversation!"
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": initial_message}
    )
    
    assert response.status_code == 200
    initial_response_data = response.json()
    conversation_id = initial_response_data["conversation_id"]
    assert conversation_id != ""
    
    # Now continue the conversation with the conversation_id
    follow_up_message = "This is a follow-up message to continue the conversation."
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "conversation_id": conversation_id,
            "message": follow_up_message
        }
    )
    
    # Verify the response
    assert response.status_code == 200
    follow_up_response_data = response.json()
    
    # Check that the same conversation ID was returned
    assert follow_up_response_data["conversation_id"] == conversation_id
    
    # Check that a response was provided
    assert "response" in follow_up_response_data
    assert follow_up_response_data["response"] != ""
    
    # Check that tool_calls is an empty list
    assert follow_up_response_data["tool_calls"] == []


def test_conversation_history_preserved_when_continuing(client):
    """Test that conversation history is preserved when continuing a conversation"""
    user_id = "test_user_456"
    
    # Create a conversation with initial message
    initial_message = "Initial message in the conversation."
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": initial_message}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    conversation_id = response_data["conversation_id"]
    assert conversation_id != ""
    
    # Add a follow-up message to the same conversation
    follow_up_message = "Follow-up message in the same conversation."
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "conversation_id": conversation_id,
            "message": follow_up_message
        }
    )
    
    assert response.status_code == 200
    
    # Verify that both messages exist in the database
    with Session(engine) as session:
        # Get all messages in the conversation
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        messages = session.exec(statement).all()
        
        # Should have at least 4 messages: initial user message, initial assistant response, 
        # follow-up user message, follow-up assistant response
        assert len(messages) >= 4
        
        # Verify the messages are in the right order and have correct roles
        user_messages = [msg for msg in messages if msg.role == "user"]
        assistant_messages = [msg for msg in messages if msg.role == "assistant"]
        
        # Should have at least 2 user messages (initial + follow-up)
        assert len(user_messages) >= 2
        
        # Should have at least 2 assistant messages (responses to both)
        assert len(assistant_messages) >= 2
        
        # Verify the content of user messages
        user_contents = [msg.content for msg in user_messages]
        assert initial_message in user_contents
        assert follow_up_message in user_contents


def test_cross_user_conversation_access_prevented(client):
    """Test that one user cannot access another user's conversation"""
    user1_id = "user_123"
    user2_id = "user_456"
    
    # User 1 creates a conversation
    user1_message = "Message from user 1."
    response = client.post(
        f"/api/{user1_id}/chat",
        json={"message": user1_message}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    conversation_id = response_data["conversation_id"]
    assert conversation_id != ""
    
    # User 2 tries to access User 1's conversation
    user2_message = "User 2 trying to access user 1's conversation."
    response = client.post(
        f"/api/{user2_id}/chat",
        json={
            "conversation_id": conversation_id,
            "message": user2_message
        }
    )
    
    # This should either return 404 (conversation not found for this user) 
    # or create a new conversation (which would have a different ID)
    if response.status_code == 200:
        new_response_data = response.json()
        # If successful, it should be a new conversation, not the original one
        assert new_response_data["conversation_id"] != conversation_id
    elif response.status_code == 404:
        # This is also valid - the conversation wasn't found for user2
        pass
    else:
        # Any other status code is unexpected
        assert False, f"Unexpected status code: {response.status_code}"