from datetime import timedelta, datetime
import os
from typing import Optional
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from models.models import User as UserModel
from schemas.auth import IUser, UserCredential, UserRegisterRequest
# Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MIMUTES = 4000

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")  # Replace with a secure secret key


class AuthRepository:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    async def authenticate_user(self, session: AsyncSession, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            print(f'GET PAYLOAD: {payload}')
            if email is None:
                raise credentials_exception
            # token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        # user = self.get_user(session=session ,token_data.username)
        # if user is None:
        #     raise credentials_exception
        # return user

    async def get_user(self, session: AsyncSession, email: str) -> IUser:
        stmt = select(UserModel).where(UserModel.email == email)
        res = await session.execute(stmt)
        user = res.scalars().first()
        if user is None:
            return None
        return IUser(id=user.id, username=user.username, email=user.email, is_active=user.is_active, hashed_password=user.hashed_password)

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> UserCredential:
        to_encode = data.copy()
        if expires_delta is not None:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        #access token
        to_encode.update({"exp": expire})
        to_encode.update({"type":"access"})
        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        #refresh_token
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MIMUTES)})
        to_encode.update({"type":"refresh"})
        refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return UserCredential(access_token=access_token, refresh_token=refresh_token, expired_at=expire.isoformat())

    async def create_user(self, data: UserModel, session: AsyncSession) -> None:
        entity = UserModel(id=uuid4(), username=data.username,
                           email=data.email, hashed_password=data.password, is_active=True)
        session.add(entity)
        await session.commit()
        return
