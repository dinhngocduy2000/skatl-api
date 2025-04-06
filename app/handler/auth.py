from schemas.auth import UserBase
from utils.exception_handler import  handle_exceptions
from controller.auth import AuthController


class AuthHandler:
    controller: AuthController
    def __init__(self,controller:AuthController):
        self.controller=controller

    @handle_exceptions()
    async def login(self, input: UserBase) -> str:
        print(f"INPUT: {input}")
        return await self.controller.verify_generate_token(input)