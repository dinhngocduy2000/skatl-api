from fastapi import APIRouter
from schemas.auth import UserCredential

from handler.auth import AuthHandler


class AuthRoute:
    router: APIRouter
    handler: AuthHandler

    def __init__(self, handler: AuthHandler):
        self.router = APIRouter()
        self.handler = handler

        self.router.add_api_route(
            path="/login", endpoint=self.handler.login,
            methods=["POST"],
            summary="Login",
            description="Login",
            response_model=str)
