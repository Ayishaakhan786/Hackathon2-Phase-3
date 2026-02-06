from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskRead
from ..services.task_service import TaskService
from .deps import get_async_session  # Removed get_current_user import for hackathon mode
# from .deps import get_current_user  # TEMPORARY: Commented out for hackathon mode - re-enable for production
from ..models.user import User


router = APIRouter()


@router.get("/{user_id}/tasks", response_model=list[TaskRead])
async def get_user_tasks(
    user_id: UUID,
    # current_user: User = Depends(get_current_user),  # TEMPORARY: Removed for hackathon mode - re-enable for production
    db_session: AsyncSession = Depends(get_async_session)
):
    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the requested user_id matches the current user's ID
    # This ensures users can only access their own tasks
    # if current_user.id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot access other user's tasks"
    #     )

    # Get all tasks for the user
    tasks = await TaskService.get_tasks_by_user_id(user_id=user_id, db_session=db_session)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: UUID,
    task_create: TaskCreate,
    # current_user: User = Depends(get_current_user),  # TEMPORARY: Removed for hackathon mode - re-enable for production
    db_session: AsyncSession = Depends(get_async_session)
):
    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the user_id in the path matches the current user's ID
    # This ensures users can only create tasks for themselves
    # if current_user.id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot create tasks for other users"
    #     )

    # Create the task for the user
    task = await TaskService.create_task(task_create=task_create, user_id=user_id, db_session=db_session)
    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    user_id: UUID,
    task_id: UUID,
    # current_user: User = Depends(get_current_user),  # TEMPORARY: Removed for hackathon mode - re-enable for production
    db_session: AsyncSession = Depends(get_async_session)
):
    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the requested user_id matches the current user's ID
    # if current_user.id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot access other user's tasks"
    #     )

    # Get the specific task
    task = await TaskService.get_task_by_id(task_id=task_id, db_session=db_session)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the task belongs to the user
    # if task.user_id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot access other user's tasks"
    #     )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_update: TaskCreate,  # Using TaskCreate for simplicity, but could create a specific update model
    # current_user: User = Depends(get_current_user),  # TEMPORARY: Removed for hackathon mode - re-enable for production
    db_session: AsyncSession = Depends(get_async_session)
):
    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the requested user_id matches the current user's ID
    # if current_user.id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot update other user's tasks"
    #     )

    # Get the existing task
    existing_task = await TaskService.get_task_by_id(task_id=task_id, db_session=db_session)

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the task belongs to the user
    # if existing_task.user_id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot update other user's tasks"
    #     )

    # Update the task
    updated_task_data = task_update.dict(exclude_unset=True)
    updated_task = await TaskService.update_task(task_id=task_id, task_update=updated_task_data, db_session=db_session)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    # current_user: User = Depends(get_current_user),  # TEMPORARY: Removed for hackathon mode - re-enable for production
    db_session: AsyncSession = Depends(get_async_session)
):
    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the requested user_id matches the current user's ID
    # if current_user.id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot delete other user's tasks"
    #     )

    # Get the existing task
    existing_task = await TaskService.get_task_by_id(task_id=task_id, db_session=db_session)

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the task belongs to the user
    # if existing_task.user_id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot delete other user's tasks"
    #     )

    # Delete the task
    success = await TaskService.delete_task(task_id=task_id, db_session=db_session)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    user_id: UUID,
    task_id: UUID,
    # current_user: User = Depends(get_current_user),  # TEMPORARY: Removed for hackathon mode - re-enable for production
    db_session: AsyncSession = Depends(get_async_session)
):
    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the requested user_id matches the current user's ID
    # if current_user.id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot update other user's tasks"
    #     )

    # Get the existing task
    existing_task = await TaskService.get_task_by_id(task_id=task_id, db_session=db_session)

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # TEMPORARY: Removed user validation for hackathon mode - re-enable for production
    # Verify that the task belongs to the user
    # if existing_task.user_id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Access forbidden: cannot update other user's tasks"
    #     )

    # Toggle the task completion
    updated_task = await TaskService.toggle_task_completion(task_id=task_id, db_session=db_session)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task