from datetime import timedelta, datetime
import os
from typing import Optional
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from common import logger
from common.cookie import get_token_from_cookie
from models.models import User as UserModel
from schemas.auth import IUser, UserCredential, UserRegisterRequest
# Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_MIMUTES = 4000

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")  # Replace with a secure secret key


class AuthRepository:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    async def extract_access(self,  token: str) -> Optional[UserCredential]:
        # extract claims from token
        try:
            claims = jwt.decode(
                token, self.secret, algorithms=[ALGORITHM]
            )
            user_id = claims["id"]
            if (user_id is not None):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

            # Add validation for role here if needed need to query database to get the latest role
            # --impl--
        except jwt.ExpiredSignatureError:
            logger.error("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            return None

        if "type" not in claims or claims["type"] != "access":
            logger.error("Invalid token")
            return None

        return UserCredential(id=user_id, access_token=token, refresh_token="", expired_at=claims["exp"])

    async def get_user(self, session: AsyncSession, email: str) -> IUser:
        stmt = select(UserModel).where(UserModel.email == email)
        res = await session.execute(stmt)
        user = res.scalars().first()
        if user is None:
            return None
        return IUser(id=user.id, username=user.username, email=user.email, is_active=user.is_active, hashed_password=user.hashed_password)

    async def create_access_token(self,  data: dict, expires_delta: Optional[timedelta] = None) -> UserCredential:
        to_encode = data.copy()
        if expires_delta is not None:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        # access token
        to_encode.update({"exp": expire})
        to_encode.update({"type": "access"})
        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        # refresh_token
        to_encode.update({"exp": datetime.utcnow() +
                         timedelta(minutes=REFRESH_TOKEN_EXPIRE_MIMUTES)})
        to_encode.update({"type": "refresh"})
        refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return UserCredential(access_token=access_token, refresh_token=refresh_token, expired_at=expire.isoformat(timespec="seconds")+"Z")

    async def create_user(self, data: UserModel, session: AsyncSession) -> None:
        entity = UserModel(id=uuid4(), username=data.username,
                           email=data.email, hashed_password=data.password, is_active=True)
        session.add(entity)
        await session.commit()
        return

   
    # async def refresh(self,token:str)->Op
