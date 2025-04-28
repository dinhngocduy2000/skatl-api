from fastapi import APIRouter, Depends
from common.auth_middleware import get_current_user
from common.cookie import get_token_from_cookie
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
            dependencies=[Depends(get_token_from_cookie), Depends(get_current_user)],
            response_model=str,
        )

      
