from typing import List
from schemas.dto.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from common.success_response import SuccessResponse
from utils.exception_handler import handle_exceptions
from controller.project import ProjectController


class ProjectHandler:
    controller: ProjectController

    def __init__(self, controller: ProjectController):
        self.controller = controller

    @handle_exceptions()
    async def create_project(self, input: ProjectCreateRequest) -> ProjectResponse:
        project = await self.controller.create_project(input)
        return ProjectResponse(**project.dict())

    @handle_exceptions()
    async def get_project(self, project_id: str) -> ProjectResponse:
        project = await self.controller.get_project(project_id)
        return ProjectResponse(**project.dict())

    @handle_exceptions()
    async def update_project(
        self, project_id: str, input: ProjectUpdateRequest
    ) -> ProjectResponse:
        project = await self.controller.update_project(project_id, input)
        return ProjectResponse(**project.dict())

    @handle_exceptions()
    async def delete_project(self, project_id: str) -> SuccessResponse:
        await self.controller.delete_project(project_id)
        return SuccessResponse(message="Project deleted successfully")

    @handle_exceptions()
    async def list_projects(self) -> List[ProjectResponse]:
        projects = await self.controller.list_projects()
        return [ProjectResponse(**project.dict()) for project in projects]
