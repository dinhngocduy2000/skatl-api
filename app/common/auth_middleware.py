# app/dependencies/auth.py
from datetime import datetime
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from common.logger import get_logger
from repository.auth import AuthRepository, IUser, UserCredential
from jose import JWTError
import jwt
ALGORITHM = "HS256"
logger = get_logger(__name__)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")  # Replace with a secure secret key


async def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access-token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token found"
        )
    return token

async def get_current_user(
    token: str = Depends(get_token_from_cookie),
) -> Optional[UserCredential]:
    logger.info(f"CHECK TOKEN: {token}")
    credential = await extract_access(token=token)
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return credential

async def extract_access(token: str) -> Optional[UserCredential]:
        # extract claims from token
        try:
            claims = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM]
            )
            user_id = claims.get("id")
            expired_at = datetime.fromtimestamp(claims.get("exp")).isoformat(timespec="seconds") +"Z"
            if user_id is None:
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
        except jwt.InvalidKeyError:
            logger.error("KEY ERROR")
            raise HTTPException(status_code=500, detail="Key error")

        if "type" not in claims or claims["type"] != "access":
            logger.error("Invalid token")
            return None

        return UserCredential(id=user_id, access_token=token, refresh_token="", expired_at=expired_at)