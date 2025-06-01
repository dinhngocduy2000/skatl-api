from typing import Optional
from schemas.dto.auth import RefreshTokenRequest, UserCredentialResponse, UserLoginRequest, UserRegisterRequest
from common.success_response import SuccessResponse
from utils.exception_handler import  handle_exceptions
from controller.auth import AuthController


class AuthHandler:
    controller: AuthController
    def __init__(self,controller:AuthController):
        self.controller=controller

    @handle_exceptions()
    async def login(self, input: UserLoginRequest) -> UserCredentialResponse:
        user_credential =  await self.controller.verify_generate_token(input)
        return UserCredentialResponse(**user_credential.dict())
    
    @handle_exceptions()
    async def register(self,input:UserRegisterRequest)->None:
        await self.controller.register_user(input)
        return SuccessResponse(message="Success")
    
    @handle_exceptions()
    async def refresh(self, input: RefreshTokenRequest) -> Optional[UserCredentialResponse]:
        user_credential = await self.controller.refresh(token=input.token)
        return UserCredentialResponse(**user_credential.dict())