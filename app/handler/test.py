from fastapi import Request
from common.success_response import SuccessResponse
from schemas.auth import UserBase, UserCredential, UserRegisterRequest
from utils.exception_handler import  handle_exceptions
from controller.auth import AuthController


class TesstHandler:
        
    @handle_exceptions()
    async def test(self, request: Request) -> str:
        cookie = request.cookies.get("access-token")
        print(f"CHECK REQUEST: {cookie}")
        return "Test"
    
    @handle_exceptions()
    async def register(self,input:UserRegisterRequest)->None:
        await self.controller.register_user(input)
        return SuccessResponse(message="Success")
    