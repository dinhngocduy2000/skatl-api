from typing import Optional
from common.success_response import SuccessResponse
from schemas.auth import RefreshTokenRequest, UserBase, UserCredential, UserRegisterRequest
from utils.exception_handler import  handle_exceptions
from controller.auth import AuthController


class AuthHandler:
    controller: AuthController
    def __init__(self,controller:AuthController):
        self.controller=controller

    @handle_exceptions()
    async def login(self, input: UserBase) -> UserCredential:
        return await self.controller.verify_generate_token(input)
    
    @handle_exceptions()
    async def register(self,input:UserRegisterRequest)->None:
        await self.controller.register_user(input)
        return SuccessResponse(message="Success")
    
    @handle_exceptions()
    async def refresh(self, input: RefreshTokenRequest) -> Optional[UserCredential]:
        return await self.controller.refresh(token=input.token)