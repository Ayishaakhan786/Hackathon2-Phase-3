"""
Contract test for POST /api/{user_id}/chat endpoint
This test verifies that the API conforms to the expected contract
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.connection import create_db_and_tables, engine
from sqlmodel import SQLModel, Session
from unittest.mock import patch


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        # Create tables for testing
        SQLModel.metadata.create_all(bind=engine)
        yield test_client
        # Clean up after test
        SQLModel.metadata.drop_all(bind=engine)


def test_chat_endpoint_contract(client):
    """Test that the chat endpoint conforms to the expected contract"""
    user_id = "test_user_123"
    
    # Mock the placeholder response to have predictable output
    with patch('src.api.chat_api.ChatResponse') as mock_response:
        mock_response.return_value = {
            "conversation_id": "test_conv_456",
            "response": "This is a test response",
            "tool_calls": []
        }
        
        # Test request without conversation_id (new conversation)
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Hello, how can you help me?"}
        )
        
        # Verify response structure
        assert response.status_code == 200
        response_data = response.json()
        
        # Check that response has the expected fields
        assert "conversation_id" in response_data
        assert "response" in response_data
        assert "tool_calls" in response_data
        assert isinstance(response_data["tool_calls"], list)
        
        # Verify conversation_id is a string
        assert isinstance(response_data["conversation_id"], str)
        
        # Verify response is a string
        assert isinstance(response_data["response"], str)
        
        # Verify tool_calls is an empty list (as specified in contract)
        assert response_data["tool_calls"] == []


def test_chat_endpoint_with_conversation_id_contract(client):
    """Test that the chat endpoint works with existing conversation_id"""
    user_id = "test_user_123"
    conversation_id = "existing_conv_789"
    
    with patch('src.api.chat_api.ChatResponse') as mock_response:
        mock_response.return_value = {
            "conversation_id": conversation_id,
            "response": "This is a test response for existing conversation",
            "tool_calls": []
        }
        
        # Test request with conversation_id (existing conversation)
        response = client.post(
            f"/api/{user_id}/chat",
            json={
                "conversation_id": conversation_id,
                "message": "Continuing the conversation..."
            }
        )
        
        # Verify response structure
        assert response.status_code == 200
        response_data = response.json()
        
        # Check that response has the expected fields
        assert "conversation_id" in response_data
        assert "response" in response_data
        assert "tool_calls" in response_data
        assert isinstance(response_data["tool_calls"], list)
        
        # Verify conversation_id matches what was sent
        assert response_data["conversation_id"] == conversation_id
        
        # Verify response is a string
        assert isinstance(response_data["response"], str)
        
        # Verify tool_calls is an empty list (as specified in contract)
        assert response_data["tool_calls"] == []


def test_chat_endpoint_missing_message_fails(client):
    """Test that the chat endpoint fails appropriately when message is missing"""
    user_id = "test_user_123"
    
    response = client.post(
        f"/api/{user_id}/chat",
        json={}  # Missing required message field
    )
    
    # Should return a validation error
    assert response.status_code == 422  # Unprocessable Entity for validation error


def test_continue_conversation_contract(client):
    """Test that the chat endpoint properly handles existing conversation IDs"""
    user_id = "test_user_123"
    conversation_id = "existing_conversation_456"
    test_message = "This is a message to continue an existing conversation."
    
    # Test request with existing conversation_id
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "conversation_id": conversation_id,
            "message": test_message
        }
    )
    
    # The response depends on whether the conversation exists in the database
    # If it doesn't exist, it should return 404
    # If it does exist, it should return 200 with updated conversation
    if response.status_code == 200:
        response_data = response.json()
        assert "conversation_id" in response_data
        assert "response" in response_data
        assert "tool_calls" in response_data
        assert isinstance(response_data["tool_calls"], list)
        
        # Verify conversation_id matches what was sent
        assert response_data["conversation_id"] == conversation_id
        
        # Verify response is a string
        assert isinstance(response_data["response"], str)
        
        # Verify tool_calls is an empty list (as specified in contract)
        assert response_data["tool_calls"] == []
    elif response.status_code == 404:
        # This is also valid if the conversation doesn't exist
        pass
    else:
        # Any other status code is unexpected
        assert False, f"Unexpected status code: {response.status_code}"


def test_invalid_conversation_access(client):
    """Test that invalid conversation access is handled properly"""
    user_id = "test_user_123"
    invalid_conversation_id = "non_existent_conversation"
    test_message = "Trying to access a non-existent conversation."
    
    # Test request with non-existent conversation_id
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "conversation_id": invalid_conversation_id,
            "message": test_message
        }
    )
    
    # Should return 404 for non-existent conversation
    assert response.status_code == 404


def test_fetch_conversation_history_contract(client):
    """Test that the API properly handles conversation history requests"""
    # This functionality is currently handled within the same endpoint
    # when continuing an existing conversation
    user_id = "test_user_123"
    conversation_id = "existing_conversation_456"
    test_message = "This is a test message to trigger history inclusion."
    
    # Test request with existing conversation_id
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "conversation_id": conversation_id,
            "message": test_message
        }
    )
    
    # The response should include the conversation history (indirectly)
    # by successfully continuing the conversation
    if response.status_code == 200:
        response_data = response.json()
        assert "conversation_id" in response_data
        assert "response" in response_data
        assert "tool_calls" in response_data
        assert isinstance(response_data["tool_calls"], list)
        
        # Verify conversation_id matches what was sent
        assert response_data["conversation_id"] == conversation_id
        
        # Verify response is a string
        assert isinstance(response_data["response"], str)
        
        # Verify tool_calls is an empty list (as specified in contract)
        assert response_data["tool_calls"] == []
    elif response.status_code == 404:
        # This is also valid if the conversation doesn't exist
        pass
    else:
        # Any other status code is unexpected
        assert False, f"Unexpected status code: {response.status_code}"