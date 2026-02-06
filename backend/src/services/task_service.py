from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.task import Task, TaskCreate
from uuid import UUID


class TaskService:
    @staticmethod
    async def create_task(*, task_create: TaskCreate, user_id: UUID, db_session: AsyncSession) -> Task:
        """
        Create a new task for a specific user.
        """
        # Create the task object with the user_id
        task = Task.model_validate(task_create, update={"user_id": user_id})
        
        # Add to database
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)
        
        return task

    @staticmethod
    async def get_task_by_id(*, task_id: UUID, db_session: AsyncSession) -> Task:
        """
        Retrieve a task by its ID.
        """
        statement = select(Task).where(Task.id == task_id)
        result = await db_session.exec(statement)
        return result.first()

    @staticmethod
    async def get_tasks_by_user_id(*, user_id: UUID, db_session: AsyncSession) -> list[Task]:
        """
        Retrieve all tasks for a specific user.
        """
        statement = select(Task).where(Task.user_id == user_id)
        result = await db_session.exec(statement)
        return result.all()

    @staticmethod
    async def update_task(*, task_id: UUID, task_update: dict, db_session: AsyncSession) -> Task:
        """
        Update a task with the provided data.
        """
        task = await TaskService.get_task_by_id(task_id=task_id, db_session=db_session)
        if not task:
            return None
        
        # Update the task with the provided data
        for key, value in task_update.items():
            setattr(task, key, value)
        
        await db_session.commit()
        await db_session.refresh(task)
        return task

    @staticmethod
    async def delete_task(*, task_id: UUID, db_session: AsyncSession) -> bool:
        """
        Delete a task by its ID.
        """
        task = await TaskService.get_task_by_id(task_id=task_id, db_session=db_session)
        if not task:
            return False
        
        await db_session.delete(task)
        await db_session.commit()
        return True

    @staticmethod
    async def toggle_task_completion(*, task_id: UUID, db_session: AsyncSession) -> Task:
        """
        Toggle the completion status of a task.
        """
        task = await TaskService.get_task_by_id(task_id=task_id, db_session=db_session)
        if not task:
            return None
        
        task.completed = not task.completed
        await db_session.commit()
        await db_session.refresh(task)
        return task