"""
MCP Tools for Task Management

This module contains the implementation of each task operation as an MCP tool.
Each tool follows the pattern:
1. Validate user ownership of resources
2. Perform database operation
3. Return structured JSON response
4. Handle errors gracefully
"""
import json
from mcp.types import Arguments, Result
from typing import Dict, Any
from contextlib import contextmanager

from ..services.task_service import (
    add_task, list_tasks, complete_task, update_task, delete_task
)
from ..db.connection import get_session
from ..models.task import TaskUpdate


@contextmanager
def get_db_session():
    """Context manager for database sessions."""
    session_gen = get_session()
    session = next(session_gen)
    try:
        yield session
    finally:
        session.close()


async def add_task_tool(arguments: Arguments) -> Result:
    """
    MCP Tool: Add a new task for a user.
    
    Args:
        arguments: Dictionary containing user_id, title, and optional description
        
    Returns:
        Result with structured JSON response
    """
    try:
        user_id = arguments["user_id"]
        title = arguments["title"]
        description = arguments.get("description", "")
        
        # Validate required parameters
        if not user_id or not title:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": "user_id and title are required"
                })
            )
        
        with get_db_session() as session:
            # Add the task using the service
            task = add_task(
                session=session,
                user_id=user_id,
                title=title,
                description=description
            )
            
            return Result.ok(
                content=json.dumps({
                    "success": True,
                    "task_id": task.id,
                    "message": "Task added successfully"
                })
            )
    except Exception as e:
        return Result.ok(
            content=json.dumps({
                "success": False,
                "message": f"Error adding task: {str(e)}"
            })
        )


async def list_tasks_tool(arguments: Arguments) -> Result:
    """
    MCP Tool: List tasks for a user with optional status filter.
    
    Args:
        arguments: Dictionary containing user_id and optional status
        
    Returns:
        Result with structured JSON response
    """
    try:
        user_id = arguments["user_id"]
        status = arguments.get("status", "all")  # Default to 'all'
        
        # Validate required parameters
        if not user_id:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": "user_id is required"
                })
            )
        
        # Validate status parameter
        valid_statuses = ["all", "pending", "completed"]
        if status not in valid_statuses:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": f"Invalid status. Valid values: {valid_statuses}"
                })
            )
        
        with get_db_session() as session:
            # List tasks using the service
            from ..services.task_service import TaskStatus
            status_enum = TaskStatus(status)
            
            tasks = list_tasks(
                session=session,
                user_id=user_id,
                status=status_enum
            )
            
            # Format tasks for response
            tasks_data = []
            for task in tasks:
                tasks_data.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description or "",
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })
            
            return Result.ok(
                content=json.dumps({
                    "success": True,
                    "tasks": tasks_data,
                    "message": f"Retrieved {len(tasks_data)} tasks"
                })
            )
    except Exception as e:
        return Result.ok(
            content=json.dumps({
                "success": False,
                "message": f"Error listing tasks: {str(e)}"
            })
        )


async def complete_task_tool(arguments: Arguments) -> Result:
    """
    MCP Tool: Mark a task as completed.
    
    Args:
        arguments: Dictionary containing user_id and task_id
        
    Returns:
        Result with structured JSON response
    """
    try:
        user_id = arguments["user_id"]
        task_id = arguments["task_id"]
        
        # Validate required parameters
        if not user_id or not task_id:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": "user_id and task_id are required"
                })
            )
        
        with get_db_session() as session:
            # Attempt to complete the task
            task = complete_task(
                session=session,
                user_id=user_id,
                task_id=task_id
            )
            
            if task:
                return Result.ok(
                    content=json.dumps({
                        "success": True,
                        "message": "Task marked as completed successfully"
                    })
                )
            else:
                return Result.ok(
                    content=json.dumps({
                        "success": False,
                        "message": "Task not found or does not belong to user"
                    })
                )
    except Exception as e:
        return Result.ok(
            content=json.dumps({
                "success": False,
                "message": f"Error completing task: {str(e)}"
            })
        )


async def update_task_tool(arguments: Arguments) -> Result:
    """
    MCP Tool: Update task details.
    
    Args:
        arguments: Dictionary containing user_id, task_id, and optional fields to update
        
    Returns:
        Result with structured JSON response
    """
    try:
        user_id = arguments["user_id"]
        task_id = arguments["task_id"]
        title = arguments.get("title")
        description = arguments.get("description")
        
        # Validate required parameters
        if not user_id or not task_id:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": "user_id and task_id are required"
                })
            )
        
        # At least one field to update must be provided
        if title is None and description is None:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": "At least one field (title or description) must be provided for update"
                })
            )
        
        # Prepare update data
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
            
        task_update = TaskUpdate(**update_data)
        
        with get_db_session() as session:
            # Attempt to update the task
            task = update_task(
                session=session,
                user_id=user_id,
                task_id=task_id,
                task_update=task_update
            )
            
            if task:
                return Result.ok(
                    content=json.dumps({
                        "success": True,
                        "message": "Task updated successfully"
                    })
                )
            else:
                return Result.ok(
                    content=json.dumps({
                        "success": False,
                        "message": "Task not found or does not belong to user"
                    })
                )
    except Exception as e:
        return Result.ok(
            content=json.dumps({
                "success": False,
                "message": f"Error updating task: {str(e)}"
            })
        )


async def delete_task_tool(arguments: Arguments) -> Result:
    """
    MCP Tool: Delete a task.
    
    Args:
        arguments: Dictionary containing user_id and task_id
        
    Returns:
        Result with structured JSON response
    """
    try:
        user_id = arguments["user_id"]
        task_id = arguments["task_id"]
        
        # Validate required parameters
        if not user_id or not task_id:
            return Result.ok(
                content=json.dumps({
                    "success": False,
                    "message": "user_id and task_id are required"
                })
            )
        
        with get_db_session() as session:
            # Attempt to delete the task
            success = delete_task(
                session=session,
                user_id=user_id,
                task_id=task_id
            )
            
            if success:
                return Result.ok(
                    content=json.dumps({
                        "success": True,
                        "message": "Task deleted successfully"
                    })
                )
            else:
                return Result.ok(
                    content=json.dumps({
                        "success": False,
                        "message": "Task not found or does not belong to user"
                    })
                )
    except Exception as e:
        return Result.ok(
            content=json.dumps({
                "success": False,
                "message": f"Error deleting task: {str(e)}"
            })
        )