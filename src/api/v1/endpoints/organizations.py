from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.sql.annotation import Annotated
from typing import List, Optional

from services.organization import OrganizationService
from depends import get_organization_service, verify_api_key
from schemas.organization import (
    OrganizationResponse,
    OrganizationCreate,
    OrganizationUpdate,
    RadiusSearchRequest,
    RectangleSearchRequest
)

router = APIRouter()


@router.get("/organizations", response_model=List[OrganizationResponse])
async def get_organizations(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)], # noqa
    authorized: Annotated[bool, Depends(verify_api_key)], # noqa

    building_id: Optional[int] = None,
    activity_id: Optional[int] = None,
    name: Optional[str] = None,
    activity_search: Optional[str] = None,
    include_subactivities: bool = False
):
    """
    Получить список организаций по фильтрам

    :param building_id:
    :param activity_id:
    :param name:
    :param activity_search:
    :param include_subactivities:

    :return: List[OrganizationResponse]
    """


    if authorized:
        filters = {}
        if building_id:
            filters['building_id'] = building_id
        if activity_id:
            filters['activity_id'] = activity_id
        if name:
            filters['name'] = name
        if activity_search:
            filters['activity_search'] = activity_search
        filters['include_subactivities'] = include_subactivities

        return await organization_service.get_organizations(filters)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.get("/organizations/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
        organization_id: int,
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)], # noqa
        authorized: bool = Depends(verify_api_key), # noqa
):
    """
    Получить организацию по id

    :param organization_id:
    :return: OrganizationResponse
    """
    if authorized:
        return await organization_service.get_organization(organization_id)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.post("/organizations", response_model=OrganizationResponse)
async def create_organization(
        organization_data: OrganizationCreate,
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)], # noqa
        authorized: bool = Depends(verify_api_key), # noqa
):
    """
    Создать организацию

    :param organization_data:

    :return: OrganizationResponse
    """
    if authorized:
        return await organization_service.create_organization(organization_data)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.put("/organizations/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
        organization_id: int,
        organization_data: OrganizationUpdate,
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)], # noqa
        authorized: bool = Depends(verify_api_key), # noqa
):
    """
    Обновить организацию

    :param organization_id:
    :param organization_data:
    :return: OrganizationResponse
    """
    if authorized:
        return await organization_service.update_organization(organization_id, organization_data)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.get("/organizations/within_radius", response_model=List[OrganizationResponse])
async def get_organizations_within_radius(

        organization_service: Annotated[OrganizationService, Depends(get_organization_service)], # noqa
        authorized: bool = Depends(verify_api_key), # noqa

        latitude: float = Query(..., description="Широта центра поиска"),
        longitude: float = Query(..., description="Долгота центра поиска"),
        radius_km: float = Query(..., gt=0, description="Радиус в километрах"),

):
    """
    Поиск в указанном радиусе поиска
    :param latitude:
    :param longitude:
    :param radius_km:

    :return:
    """


    if authorized:
        return await organization_service.get_organizations_within_radius(
            latitude,
            longitude,
            radius_km
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.get("/organizations/within_rectangle", response_model=List[OrganizationResponse])
async def get_organizations_within_rectangle(
        request: RectangleSearchRequest,
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)], # noqa
        authorized: bool = Depends(verify_api_key), # noqa
):
    """
    Поиск организаций в указанной области
    :param request:

    :return: List[OrganizationResponse]
    """
    if authorized:
        return await organization_service.get_organizations_within_rectangle(
            request.min_lat,
            request.max_lat,
            request.min_lon,
            request.max_lon
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
