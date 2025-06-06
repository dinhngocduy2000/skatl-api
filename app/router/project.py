from typing import List
from fastapi import APIRouter, Depends
from common.auth_middleware import get_current_user
from common.cookie import get_token_from_cookie
from common.success_response import SuccessResponse
from handler.project import ProjectHandler
from schemas.dto.project import ProjectResponse


class ProjectRoute:
    router: APIRouter
    handler: ProjectHandler

    def __init__(self, handler: ProjectHandler):
        self.router = APIRouter()
        self.handler = handler

        self.router.add_api_route(
            path="/projects",
            endpoint=self.handler.create_project,
            methods=["POST"],
            summary="Create a new project",
            description="Create a new project",
            dependencies=[Depends(get_token_from_cookie), Depends(get_current_user)],
            response_model=ProjectResponse,
        )

        self.router.add_api_route(
            path="/projects/{project_id}",
            endpoint=self.handler.get_project,
            methods=["GET"],
            summary="Get a project by ID",
            description="Get a project by ID",
            dependencies=[Depends(get_token_from_cookie), Depends(get_current_user)],
            response_model=ProjectResponse,
        )

        self.router.add_api_route(
            path="/projects/{project_id}",
            endpoint=self.handler.update_project,
            methods=["PUT"],
            summary="Update a project by ID",
            description="Update a project by ID",
            dependencies=[Depends(get_token_from_cookie), Depends(get_current_user)],
            response_model=ProjectResponse,
        )

        self.router.add_api_route(
            path="/projects/{project_id}",
            endpoint=self.handler.delete_project,
            methods=["DELETE"],
            summary="Delete a project by ID",
            description="Delete a project by ID",
            dependencies=[Depends(get_token_from_cookie), Depends(get_current_user)],
            response_model=SuccessResponse,
        )

        self.router.add_api_route(
            path="/projects",
            endpoint=self.handler.list_projects,
            methods=["GET"],
            summary="List all projects",
            description="List all projects",
            dependencies=[Depends(get_token_from_cookie), Depends(get_current_user)],
            response_model=List[ProjectResponse],
        )
