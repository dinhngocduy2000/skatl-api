
from typing import Optional
from uuid import UUID
from schemas.base import BaseModelDict


class IUser(BaseModelDict):
    id: Optional[UUID] = None
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    hashed_password: Optional[str] = None