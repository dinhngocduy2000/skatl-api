from datetime import timedelta
from fastapi import HTTPException, status
from repository.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.exception_handler import ServiceException
from schemas.auth import UserBase
from repository.registry import Registry
from sqlalchemy.ext.asyncio import AsyncSession


class AuthController:
    repo: Registry

    def __init__(self, repo: Registry):
        self.repo = repo

    async def verify_generate_token(self, input: UserBase):
        async def _verify_generate_token(session: AsyncSession):
            user = await self.repo.auth_repo().authenticate_user(session=session, email=input.email)
            if user is None: 
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.repo.auth_repo().create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )   
            return access_token
            
        return await self.repo.do_tx(_verify_generate_token)
        
    # async def authenticate_user()
