from fastapi import APIRouter, Depends
from sqlalchemy.sql.annotation import Annotated

from services.organization import OrganizationService
from depends import get_organization_service, verify_api_key
from schemas.organization import OrganizationResponse
from typing import List

router = APIRouter()


@router.get("/organizations", response_model=List[OrganizationResponse])
async def get_organizations(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    authorized: bool = Depends(verify_api_key),
):
    pass

@router.get("/organizations/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: int,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    authorized: bool = Depends(verify_api_key),
):
    pass

@router.post("/organizations", response_model=OrganizationResponse)
async def create_organization(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    authorized: bool = Depends(verify_api_key),
):
    pass

@router.put("/organizations/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: int,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    authorized: bool = Depends(verify_api_key),
):
    pass
