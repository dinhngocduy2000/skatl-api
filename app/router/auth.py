from fastapi import APIRouter
from common.success_response import SuccessResponse
from schemas.auth import UserCredential

from handler.auth import AuthHandler


class AuthRoute:
    router: APIRouter
    handler: AuthHandler

    def __init__(self, handler: AuthHandler):
        self.router = APIRouter()
        self.handler = handler

        self.router.add_api_route(
            path="/login",
            endpoint=self.handler.login,
            methods=["POST"],
            summary="Login",
            description="Login",
            response_model=UserCredential
        )

        self.router.add_api_route(
            path="/register",
            endpoint=self.handler.register,
            methods=["POST"],
            response_model=SuccessResponse,
            summary="Register",
            description="Register"
        )

        self.router.add_api_route(
            path="/refresh",
            endpoint=self.handler.refresh,
            methods=["POST"],
            response_model=UserCredential,
            summary="Refresh token",
            description="Refresh token"
        )