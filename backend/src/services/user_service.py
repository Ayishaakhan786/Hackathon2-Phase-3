from sqlmodel import Session, select
from src.models.user import User, UserCreate
from src.core.security import get_password_hash, verify_password
from typing import Optional


class UserService:
    @staticmethod
    async def create_user(*, user_create: UserCreate, db_session: Session) -> User:
        """
        Create a new user with hashed password.
        """
        # Hash the password
        hashed_password = get_password_hash(user_create.password)
        
        # Create the user object
        user = User(
            email=user_create.email,
            hashed_password=hashed_password
        )
        
        # Add to database
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        return user

    @staticmethod
    async def get_user_by_email(*, email: str, db_session: Session) -> Optional[User]:
        """
        Retrieve a user by email.
        """
        statement = select(User).where(User.email == email)
        result = await db_session.exec(statement)
        return result.first()

    @staticmethod
    async def authenticate_user(*, email: str, password: str, db_session: Session) -> Optional[User]:
        """
        Authenticate a user by email and password.
        """
        user = await UserService.get_user_by_email(email=email, db_session=db_session)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user