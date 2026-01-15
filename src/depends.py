from repositories.activity import ActivityRepository
from services import organization
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db_session
from repositories.organization import (
    OrganizationRepository,
)
from fastapi import security
from fastapi.security import HTTPBearer

from config import settings


def verify_api_key(credentials: security.HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> bool:
    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        if credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")

        if credentials.credentials != settings.api_key:
            raise HTTPException(status_code=403, detail="Invalid API Key")

        return True
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header")



def get_organization_repository() -> OrganizationRepository:
    return OrganizationRepository()

def get_activity_repository() -> ActivityRepository:
    return ActivityRepository()


def get_organization_service(
    session: AsyncSession = Depends(get_db_session),
    repository: OrganizationRepository = Depends(get_organization_repository),
    activity_repository: ActivityRepository = Depends(get_activity_repository)
) -> organization.OrganizationService:
    return organization.OrganizationService(repository, activity_repository, session)
