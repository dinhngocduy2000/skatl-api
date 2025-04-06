from enum import Enum
from typing import Any, Dict
from pydantic_settings import BaseSettings

class AppEnvTypes(Enum):
    PROD: str = "prod"
    DEV: str = "dev"
    TEST: str = "test"

class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes= AppEnvTypes.DEV
    class Config:
        env_file="../.env"
        extra="ignore"
        

class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "SkatL application"
    version: str = "0.0.0"
    pg_url: str

      
    @property
    def fastapi_kwargs(self)->Dict[str,Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }
    
settings = AppSettings()
print(f"Loaded PG_URL: {settings.pg_url}")