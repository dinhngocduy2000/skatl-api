from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from schemas.dto.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from repository.registry import Registry
from sqlalchemy.ext.asyncio import AsyncSession


class ProjectController:
    repo: Registry

    def __init__(self, repo: Registry):
        self.repo = repo

    async def create_project(self, input: ProjectCreateRequest) -> ProjectResponse:
        async def _create_project(session: AsyncSession) -> ProjectResponse:
            project = await self.repo.project_repo().create_project(input, session)
            return ProjectResponse(**project.dict())

        return await self.repo.do_tx(_create_project)

    async def get_project(self, project_id: UUID) -> ProjectResponse:
        async def _get_project(session: AsyncSession) -> ProjectResponse:
            project = await self.repo.project_repo().get_project(session, project_id)
            if project is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
                )
            return ProjectResponse(**project.dict())

        return await self.repo.do_tx(_get_project)

    async def update_project(
        self, project_id: UUID, input: ProjectUpdateRequest
    ) -> ProjectResponse:
        async def _update_project(session: AsyncSession) -> ProjectResponse:
            project = await self.repo.project_repo().update_project(
                session, project_id, input
            )
            if project is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
                )
            return ProjectResponse(**project.dict())

        return await self.repo.do_tx(_update_project)

    async def delete_project(self, project_id: UUID) -> None:
        async def _delete_project(session: AsyncSession) -> None:
            project = await self.repo.project_repo().delete_project(session, project_id)
            if project is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
                )

        return await self.repo.do_tx(_delete_project)

    async def list_projects(self) -> List[ProjectResponse]:
        async def _list_projects(session: AsyncSession) -> List[ProjectResponse]:
            projects = await self.repo.project_repo().list_projects(session)
            return [ProjectResponse(**project.dict()) for project in projects]

        return await self.repo.do_tx(_list_projects)
