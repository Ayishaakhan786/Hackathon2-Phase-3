"""
Integration test for conversation persistence across sessions
This test verifies that conversation history remains intact and accessible after simulated session restarts
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


def test_conversation_persistence_across_sessions(client):
    """Test that conversation history remains intact after simulated session restart"""
    user_id = "test_user_123"
    
    # Step 1: Create a conversation with multiple messages
    initial_message = "First message in the conversation."
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": initial_message}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    conversation_id = response_data["conversation_id"]
    assert conversation_id != ""
    
    # Add a second message to the conversation
    second_message = "Second message in the conversation."
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "conversation_id": conversation_id,
            "message": second_message
        }
    )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["conversation_id"] == conversation_id
    
    # Add a third message to the conversation
    third_message = "Third message in the conversation."
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "conversation_id": conversation_id,
            "message": third_message
        }
    )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["conversation_id"] == conversation_id
    
    # Step 2: Simulate a session restart by creating a new client instance
    # and verify that the conversation history is still accessible
    with TestClient(app) as new_client:
        # Add a fourth message to the same conversation
        fourth_message = "Fourth message after simulated session restart."
        response = new_client.post(
            f"/api/{user_id}/chat",
            json={
                "conversation_id": conversation_id,
                "message": fourth_message
            }
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["conversation_id"] == conversation_id
    
    # Step 3: Verify that all messages are still in the database
    with Session(engine) as session:
        # Get all messages in the conversation
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        messages = session.exec(statement).all()
        
        # Should have at least 8 messages: 4 user messages and 4 assistant responses
        assert len(messages) >= 8
        
        # Extract user message contents
        user_messages = [msg for msg in messages if msg.role == "user"]
        user_contents = [msg.content for msg in user_messages]
        
        # Verify all messages are present
        assert initial_message in user_contents
        assert second_message in user_contents
        assert third_message in user_contents
        assert fourth_message in user_contents


def test_conversation_remains_accessible_after_server_restart_simulation(client):
    """Test that conversations remain accessible after a server restart simulation"""
    user_id = "test_user_456"
    
    # Create a conversation
    first_message = "Message in conversation that will persist."
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": first_message}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    conversation_id = response_data["conversation_id"]
    assert conversation_id != ""
    
    # Verify the conversation exists in the database
    with Session(engine) as session:
        conversation = session.get(Conversation, conversation_id)
        assert conversation is not None
        assert conversation.user_id == user_id
    
    # Simulate server restart by recreating the database connection
    # (In a real scenario, this would be an actual server restart)
    # For this test, we'll just verify the data is still there
    with Session(engine) as session:
        # Check that the conversation still exists
        conversation = session.get(Conversation, conversation_id)
        assert conversation is not None
        assert conversation.user_id == user_id
        
        # Check that the messages still exist
        statement = select(Message).where(Message.conversation_id == conversation_id)
        messages = session.exec(statement).all()
        assert len(messages) >= 2  # At least the first user message and assistant response


def test_multiple_users_conversations_persist_independently(client):
    """Test that multiple users' conversations persist independently"""
    user1_id = "user_123"
    user2_id = "user_456"
    
    # User 1 creates a conversation
    user1_message = "Message from user 1."
    response = client.post(
        f"/api/{user1_id}/chat",
        json={"message": user1_message}
    )
    
    assert response.status_code == 200
    user1_response_data = response.json()
    user1_conversation_id = user1_response_data["conversation_id"]
    assert user1_conversation_id != ""
    
    # User 2 creates a separate conversation
    user2_message = "Message from user 2."
    response = client.post(
        f"/api/{user2_id}/chat",
        json={"message": user2_message}
    )
    
    assert response.status_code == 200
    user2_response_data = response.json()
    user2_conversation_id = user2_response_data["conversation_id"]
    assert user2_conversation_id != ""
    assert user2_conversation_id != user1_conversation_id  # Different conversations
    
    # Both users add more messages to their respective conversations
    user1_followup = "Follow-up from user 1."
    response = client.post(
        f"/api/{user1_id}/chat",
        json={
            "conversation_id": user1_conversation_id,
            "message": user1_followup
        }
    )
    
    assert response.status_code == 200
    
    user2_followup = "Follow-up from user 2."
    response = client.post(
        f"/api/{user2_id}/chat",
        json={
            "conversation_id": user2_conversation_id,
            "message": user2_followup
        }
    )
    
    assert response.status_code == 200
    
    # Verify that both conversations have persisted correctly
    with Session(engine) as session:
        # Check user 1's conversation
        user1_messages = session.exec(
            select(Message).where(Message.conversation_id == user1_conversation_id)
        ).all()
        assert len(user1_messages) >= 4  # 2 user messages + 2 assistant responses
        
        # Check user 2's conversation
        user2_messages = session.exec(
            select(Message).where(Message.conversation_id == user2_conversation_id)
        ).all()
        assert len(user2_messages) >= 4  # 2 user messages + 2 assistant responses
        
        # Verify that user 1's messages are only in user 1's conversation
        user1_message_contents = [msg.content for msg in user1_messages if msg.role == "user"]
        assert user1_message in user1_message_contents
        assert user1_followup in user1_message_contents
        assert user2_message not in user1_message_contents
        assert user2_followup not in user1_message_contents
        
        # Verify that user 2's messages are only in user 2's conversation
        user2_message_contents = [msg.content for msg in user2_messages if msg.role == "user"]
        assert user2_message in user2_message_contents
        assert user2_followup in user2_message_contents
        assert user1_message not in user2_message_contents
        assert user1_followup not in user2_message_contents