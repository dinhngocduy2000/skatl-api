from fastapi import APIRouter
from common.success_response import SuccessResponse

from handler.test import TesstHandler


class TestRoute:
    router: APIRouter
    handler: TesstHandler

    def __init__(self, handler: TesstHandler):
        self.router = APIRouter()
        self.handler = handler

        self.router.add_api_route(
            path="/test",
            endpoint=self.handler.test,
            methods=["GET"],
            summary="Login",
            description="Login",
            response_model=str
        )

        self.router.add_api_route(
            path="/register",
            endpoint=self.handler.register,
            methods=["POST"],
            response_model=SuccessResponse,
            summary="Register",
            description="Register"
        )
