from schemas.auth import UserBase
from repository.registry import Registry
from sqlalchemy.ext.asyncio import AsyncSession

class AuthController:
    repo:Registry

    def __init__(self,repo:Registry):
        self.repo=repo

    async def verify_generate_token(self,input:UserBase):
        async def _verify_generate_token(session:AsyncSession):
            pass