from datetime import timedelta
import os
from typing import Optional
from uuid import UUID
import bcrypt
from dotenv import load_dotenv
from fastapi import HTTPException, status
import jwt
from common.logger import get_logger
from repository.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.exception_handler import ServiceException
from schemas.auth import UserBase, UserCredential, UserRegisterRequest
from repository.registry import Registry
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")  # Replace with a secure secret key
ALGORITHM = "HS256"


class AuthController:
    repo: Registry

    def __init__(self, repo: Registry):
        self.repo = repo

    async def verify_generate_token(self, input: UserBase) -> UserCredential:
        async def _verify_generate_token(session: AsyncSession) -> UserCredential:
            user = await self.repo.auth_repo().get_user(session=session, email=input.email)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
            password_valid = bcrypt.checkpw(input.password.encode(
                "utf-8"), user.hashed_password.encode("utf-8"))
            if not password_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

            user_credential = await self.repo.auth_repo().create_access_token(
                data=UserBase(email=input.email), expires_delta=access_token_expires, user_id=user.id
            )
            return UserCredential(id=user.id, access_token=user_credential.access_token, expired_at=user_credential.expired_at, refresh_token=user_credential.refresh_token)

        return await self.repo.do_tx(_verify_generate_token)

    async def register_user(self, input: UserRegisterRequest):
        async def _register_user(session: AsyncSession):
            user = await self.repo.auth_repo().get_user(session=session, email=input.email)
            if user is not None:
                raise ServiceException(
                    detail="An account with this email address already exists!")

            hash_password = bcrypt.hashpw(input.password.encode(
                "utf-8"), bcrypt.gensalt()).decode("utf-8")
            data = UserRegisterRequest(
                email=input.email, username=input.username, password=hash_password)

            await self.repo.auth_repo().create_user(data, session)
            return
        return await self.repo.do_tx(_register_user)

    async def refresh(self, token: str) -> Optional[UserCredential]:
        logger.info(f'CHECK REFRESH TOKEN: {token}')
        # extract claims from token
        try:
            claims = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            logger.error("Token expired")
            raise ServiceException(detail="Invalid token")
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            raise ServiceException(detail="Invalid token")

        # check if type exists in claims and is refresh
        if "type" not in claims or claims["type"] != "refresh":
            logger.error("Invalid token")
            raise ServiceException(detail="Invalid token")
        user_id = UUID(claims.get("id"))
        user_email = str(claims.get("email"))
        access_token_expires = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        logger.info(f"CHECK EMAIL: {user_email}")
        user_credential = await self.repo.auth_repo().create_access_token(
            user_id=user_id,
            data=UserBase(email=user_email),
            expires_delta=access_token_expires)
        return user_credential
