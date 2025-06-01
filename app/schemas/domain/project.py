from typing import Optional
from uuid import UUID
from schemas.domain.common import QueryBase
from schemas.base import BaseModelDict


class IProject(BaseModelDict):
    id: UUID
    project_name: str = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class ProjectQuery(QueryBase):
    id: Optional[UUID] = None
    name: Optional[str] = None
    name_like: Optional[str] = None
    

class ProjectCreate(BaseModelDict):
    project_name: str
    description: Optional[str] = None