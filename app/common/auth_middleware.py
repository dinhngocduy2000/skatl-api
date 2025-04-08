from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from dependency_injector.wiring import Provide, inject
from repository.auth import AuthRepository


def auth_middleware():
    @inject
    async def extract_requester(
        auth_repository: AuthRepository,
        bearer: HTTPBearer = Depends(HTTPBearer(scheme_name="Authorization")),
    ) -> str:
        credential: Optional[str] = await auth_repository.extract_access(
           token=bearer.credentials
        )
        if credential is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return credential

    return extract_requester