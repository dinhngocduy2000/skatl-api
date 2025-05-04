import os
from typing import Optional
from uuid import uuid4
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from schemas.domain.auth import IUser
from common.logger import get_logger
from models.models import User as UserModel
logger = get_logger(__name__)
class AuthRepository:

    async def get_user(self, session: AsyncSession, email: str) -> IUser:
        stmt = select(UserModel).where(UserModel.email == email)
        res = await session.execute(stmt)
        user = res.scalars().first()
        if user is None:
            return None
        return IUser(id=user.id, username=user.username, email=user.email, is_active=user.is_active, hashed_password=user.hashed_password)


    async def create_user(self, data: UserModel, session: AsyncSession) -> None:
        entity = UserModel(id=uuid4(), username=data.username,
                           email=data.email, hashed_password=data.password, is_active=True)
        session.add(entity)
        await session.commit()
        return

    # async def refresh(self,token:str)->Op
