from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class IUser(BaseModel):
    id: UUID
    username: str
    email: str
    is_active: bool


class UserBase(BaseModel):
    email: str = Field("", description="user's email")
    password: str = Field("", description="password")


class UserCredential(UserBase):
    id: UUID = Field(None, description="User ID")
    created_at: datetime = Field(None, description="User created at")
    updated_at: datetime = Field(None, description="User updated at")
    access_token: str = Field("", description="access_token")
    refresh_token: str = Field("", description="refresh_token")
