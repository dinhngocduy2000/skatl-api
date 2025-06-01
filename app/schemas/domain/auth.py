from typing import Optional
from uuid import UUID

from pydantic import Field
from schemas.base import BaseModelDict



class UserBase(BaseModelDict):
    email: str = Field("", description="user's email",)
    password: Optional[str] = Field(description="password", default=None)

class UserRegister(UserBase):
    username:Optional[str] = Field(description="username", default=None)

class UserCredential(BaseModelDict):
    id: UUID = Field(None, description="User ID")
    access_token: str = Field("", description="access_token")
    refresh_token: str = Field("", description="refresh_token")
    expired_at:str = Field("",description="Expired token time")
