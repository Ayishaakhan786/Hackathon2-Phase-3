from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class BaseSQLModel(SQLModel):
    """Base model for all SQLModel classes"""
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None