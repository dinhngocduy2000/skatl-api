from schemas.base import BaseModelDict
from schemas.domain.auth import IUser, UserBase, UserCredential, UserRegister


class IUserResponse(IUser):
    class Config:
        json_schema_extra = {
            "example": {
                "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "username": "username",
                "email": "email",
                "is_active": "true"
            }
        }


class UserRegisterRequest(UserRegister):
    class Config:
        json_schema_extra = {
            "example": {
                "email": "email@email.com",
                "password": "password",
                "username": "username"
            }
        }


class UserLoginRequest(UserBase):
    class Config:
        json_schema_extra = {
            "example": {
                "email": "email@email.com",
                "password": "password",
            }
        }


class UserCredentialResponse(UserCredential):
    class Config:
        json_schema_extra = {
            "example": {
                "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "access_token": "",
                "refresh_token": "",
                "expired_at": ""
            }
        }

class RefreshTokenRequest(BaseModelDict):
    token: str
    class Config:
        json_schema_extra = {
            "example": {
                "token": ""
            }
        }