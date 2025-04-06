from datetime import timedelta, datetime
import os
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from models.models import User as UserModel
from schemas.auth import IUser
from jose import jwt
# Configuration 
SECRET_KEY = os.getenv("SECRET_KEY")  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthRepository:

    async def authenticate_user(self, session: AsyncSession, email: str) -> IUser:
        stmt = select(UserModel).where(UserModel.email == email)
        res = await session.execute(stmt)
        user = res.scalars().first()
        if user is None:
            return None
        return IUser(id=user.id, username=user.username, email=user.email, is_active=user.is_active)

    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt