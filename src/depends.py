from services import organization
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db_session
from repositories.organization import (
    OrganizationRepository,
)

from config import settings


def verify_api_key(authorization: str = Header(None)) -> bool:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")

        if token != settings.api_key:
            raise HTTPException(status_code=403, detail="Invalid API Key")

        return True
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")


def get_organization_repository() -> OrganizationRepository:
    return OrganizationRepository()


def get_organization_service(
    session: AsyncSession = Depends(get_db_session),
    repository: OrganizationRepository = Depends(get_organization_repository)
) -> organization.OrganizationService:
    return organization.OrganizationService(repository, session)
