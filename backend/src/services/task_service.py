from datetime import datetime
from typing import List, Optional
from sqlmodel import select, Session
from enum import Enum

from ..models.task import Task, TaskCreate, TaskUpdate


class TaskStatus(str(Enum):
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"


def add_task(*, session: Session, user_id: str, title: str, description: Optional[str] = None) -> Task:
    """
    Add a new task for the given user.
    
    Args:
        session: Database session
        user_id: ID of the user creating the task
        title: Title of the task
        description: Optional description of the task
        
    Returns:
        The created Task object
    """
    task = Task(user_id=user_id, title=title, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def list_tasks(*, session: Session, user_id: str, status: TaskStatus = TaskStatus.ALL) -> List[Task]:
    """
    List tasks for a specific user, optionally filtered by status.
    
    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve
        status: Filter by task status (all, pending, completed)
        
    Returns:
        List of Task objects matching the criteria
    """
    statement = select(Task).where(Task.user_id == user_id)
    
    if status == TaskStatus.PENDING:
        statement = statement.where(Task.completed == False)
    elif status == TaskStatus.COMPLETED:
        statement = statement.where(Task.completed == True)
    
    statement = statement.order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()
    return tasks


def complete_task(*, session: Session, user_id: str, task_id: str) -> Optional[Task]:
    """
    Mark a task as completed.
    
    Args:
        session: Database session
        user_id: ID of the user who owns the task
        task_id: ID of the task to mark as completed
        
    Returns:
        The updated Task object if found and owned by the user, None otherwise
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    
    if task:
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
    return None


def update_task(*, session: Session, user_id: str, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update a task's details.
    
    Args:
        session: Database session
        user_id: ID of the user who owns the task
        task_id: ID of the task to update
        task_update: TaskUpdate object with fields to update
        
    Returns:
        The updated Task object if found and owned by the user, None otherwise
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    
    if task:
        # Apply updates
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.completed is not None:
            task.completed = task_update.completed
            
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
    return None


def delete_task(*, session: Session, user_id: str, task_id: str) -> bool:
    """
    Delete a task.
    
    Args:
        session: Database session
        user_id: ID of the user who owns the task
        task_id: ID of the task to delete
        
    Returns:
        True if the task was found and deleted, False otherwise
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    
    if task:
        session.delete(task)
        session.commit()
        return True
    
    return False