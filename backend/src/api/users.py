from fastapi import APIRouter, Depends, HTTPException, status
from src.models.user import UserRead
from src.api.deps import get_current_user
from src.models.user import User
import uuid


router = APIRouter()


@router.get("/{user_id}", response_model=UserRead)
async def get_user_profile(
    user_id: str,  # Will be converted to UUID in the implementation
    current_user: User = Depends(get_current_user)
):
    # Verify that the requested user_id matches the current user's ID
    # This ensures users can only access their own profiles
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: cannot access other user's profile"
        )
    
    # Return the current user's information (they are the same person)
    return current_user