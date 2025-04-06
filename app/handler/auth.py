from app.schemas.auth import UserBase
from app.utils.exception_handler import exception_handler
from controller.auth import AuthController


class AuthHandler:
    controller: AuthController
    def __init__(self,controller:AuthController):
        self.controller=controller

    @exception_handler
    async def login(self, credential: UserBase) -> str:
        return "Login success"