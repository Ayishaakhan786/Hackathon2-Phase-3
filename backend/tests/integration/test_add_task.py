"""
Integration test for adding new tasks
This test verifies that the full flow of adding a new task works correctly
"""
import pytest
from unittest.mock import patch, MagicMock
from src.mcp.tools import add_task_tool
from mcp.types import Arguments
from src.models.task import Task


@pytest.mark.asyncio
async def test_add_new_task_integration():
    """Test the full flow of adding a new task via the MCP tool"""
    # Mock arguments
    arguments = Arguments({
        "user_id": "user123", 
        "title": "Buy groceries", 
        "description": "Milk, bread, eggs, and fruits"
    })
    
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
            mock_task.user_id = "user123"
            mock_task.title = "Buy groceries"
            mock_task.description = "Milk, bread, eggs, and fruits"
            mock_task.completed = False
            mock_add_task.return_value = mock_task
            
            # Call the tool
            result = await add_task_tool(arguments)
            
            # Verify the result
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"task_id": "task456"' in result.content
            assert '"Task added successfully"' in result.content
            
            # Verify that add_task was called with correct parameters
            mock_add_task.assert_called_once_with(
                session=mock_session,
                user_id="user123",
                title="Buy groceries",
                description="Milk, bread, eggs, and fruits"
            )


@pytest.mark.asyncio
async def test_add_new_task_without_description_integration():
    """Test adding a task without a description"""
    # Mock arguments without description
    arguments = Arguments({
        "user_id": "user123", 
        "title": "Complete project"
    })
    
    # Mock the database session context manager
    with patch("src.mcp.tools.get_db_session") as mock_get_session:
        # Create a mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock the add_task function to return a task
        with patch("src.mcp.tools.add_task") as mock_add_task:
            # Create a mock task object
            mock_task = MagicMock()
            mock_task.id = "task789"
            mock_task.user_id = "user123"
            mock_task.title = "Complete project"
            mock_task.description = ""  # Default empty string
            mock_task.completed = False
            mock_add_task.return_value = mock_task
            
            # Call the tool
            result = await add_task_tool(arguments)
            
            # Verify the result
            assert result.content is not None
            assert '"success": true' in result.content
            assert '"task_id": "task789"' in result.content
            assert '"Task added successfully"' in result.content
            
            # Verify that add_task was called with correct parameters
            mock_add_task.assert_called_once_with(
                session=mock_session,
                user_id="user123",
                title="Complete project",
                description=""
            )