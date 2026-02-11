"""
Contract test for MCP tools
This test verifies that the MCP tools conform to the expected contract
"""
import pytest
from unittest.mock import patch, MagicMock
from src.mcp.tools import (
    add_task_tool, list_tasks_tool, complete_task_tool, 
    update_task_tool, delete_task_tool
)
from mcp.types import Arguments


@pytest.mark.asyncio
async def test_add_task_contract_success():
    """Test that the add_task tool returns the expected response format on success"""
    # Mock arguments
    arguments = Arguments({"user_id": "user123", "title": "Test task", "description": "Test description"})
    
    # Mock the database session context manager
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        # Create a mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the add_task function to return a task
        with patch("src.mcp.tools.add_task") as mock_add_task:
            # Create a mock task object
            mock_task = MagicMock()
            mock_task.id = "task456"
            mock_add_task.return_value = mock_task
            
            # Call the tool
            result = await add_task_tool(arguments)
            
            # Verify the result
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"task_id": "task456"' in result.content
            assert '"Task added successfully"' in result.content


@pytest.mark.asyncio
async def test_add_task_contract_missing_user_id():
    """Test that the add_task tool handles missing user_id gracefully"""
    # Mock arguments with missing user_id
    arguments = Arguments({"title": "Test task"})
    
    # Call the tool
    result = await add_task_tool(arguments)
    
    # Verify the result
    assert result.content is not None
    assert '"success": false' in result.content
    assert "user_id and title are required" in result.content


@pytest.mark.asyncio
async def test_add_task_contract_missing_title():
    """Test that the add_task tool handles missing title gracefully"""
    # Mock arguments with missing title
    arguments = Arguments({"user_id": "user123"})
    
    # Call the tool
    result = await add_task_tool(arguments)
    
    # Verify the result
    assert result.content is not None
    assert '"success": false' in result.content
    assert "user_id and title are required" in result.content


@pytest.mark.asyncio
async def test_add_task_contract_exception_handling():
    """Test that the add_task tool handles exceptions gracefully"""
    # Mock arguments
    arguments = Arguments({"user_id": "user123", "title": "Test task"})
    
    # Mock the database session to raise an exception
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        mock_get_session.return_value.__enter__.side_effect = Exception("Database error")
        
        # Call the tool
        result = await add_task_tool(arguments)
        
        # Verify the result
        assert result.content is not None
        assert '"success": false' in result.content
        assert "Error adding task:" in result.content


@pytest.mark.asyncio
async def test_list_tasks_contract_success():
    """Test that the list_tasks tool returns the expected response format on success"""
    # Mock arguments
    arguments = Arguments({"user_id": "user123", "status": "pending"})
    
    # Mock the database session context manager
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        # Create a mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the list_tasks function to return tasks
        with patch("src.mcp.tools.list_tasks") as mock_list_tasks:
            # Create mock task objects
            mock_task = MagicMock()
            mock_task.id = "task456"
            mock_task.user_id = "user123"
            mock_task.title = "Test task"
            mock_task.description = "Test description"
            mock_task.completed = False
            mock_task.created_at = "2023-01-01T00:00:00"
            mock_task.updated_at = "2023-01-01T00:00:00"
            mock_list_tasks.return_value = [mock_task]
            
            # Call the tool
            result = await list_tasks_tool(arguments)
            
            # Verify the result
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"tasks"' in result.content
            assert '"Retrieved 1 tasks"' in result.content


@pytest.mark.asyncio
async def test_complete_task_contract_success():
    """Test that the complete_task tool returns the expected response format on success"""
    # Mock arguments
    arguments = Arguments({"user_id": "user123", "task_id": "task456"})
    
    # Mock the database session context manager
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        # Create a mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the complete_task function to return a task
        with patch("src.mcp.tools.complete_task") as mock_complete_task:
            # Create a mock task object
            mock_task = MagicMock()
            mock_task.id = "task456"
            mock_task.completed = True
            mock_complete_task.return_value = mock_task
            
            # Call the tool
            result = await complete_task_tool(arguments)
            
            # Verify the result
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"Task marked as completed successfully"' in result.content


@pytest.mark.asyncio
async def test_update_task_contract_success():
    """Test that the update_task tool returns the expected response format on success"""
    # Mock arguments
    arguments = Arguments({"user_id": "user123", "task_id": "task456", "title": "Updated title"})
    
    # Mock the database session context manager
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        # Create a mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the update_task function to return a task
        with patch("src.mcp.tools.update_task") as mock_update_task:
            # Create a mock task object
            mock_task = MagicMock()
            mock_task.id = "task456"
            mock_update_task.return_value = mock_task
            
            # Call the tool
            result = await update_task_tool(arguments)
            
            # Verify the result
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"Task updated successfully"' in result.content


@pytest.mark.asyncio
async def test_delete_task_contract_success():
    """Test that the delete_task tool returns the expected response format on success"""
    # Mock arguments
    arguments = Arguments({"user_id": "user123", "task_id": "task456"})
    
    # Mock the database session context manager
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        # Create a mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the delete_task function to return success
        with patch("src.mcp.tools.delete_task") as mock_delete_task:
            # Set return value to True for success
            mock_delete_task.return_value = True
            
            # Call the tool
            result = await delete_task_tool(arguments)
            
            # Verify the result
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"Task deleted successfully"' in result.content