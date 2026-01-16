from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import List, Optional, Annotated

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

    :param building_id: id здания

    :param activity_id: id деятельности

    :param name: название организации

    :param activity_search:

    :param include_subactivities:  связанные поддеятельностью

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


@router.get("/organizations/within_radius", response_model=List[OrganizationResponse])
async def get_organizations_within_radius(

        organization_service: Annotated[OrganizationService, Depends(get_organization_service)], # noqa
        authorized: Annotated[bool, Depends(verify_api_key)], # noqa

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
        print(latitude,
            longitude,
            radius_km)
        return await organization_service.get_organizations_within_radius(
            latitude,
            longitude,
            radius_km
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")



@router.get("/organizations/within_rectangle", response_model=List[OrganizationResponse])
async def get_organizations_within_rectangle(
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)], # noqa
        authorized: Annotated[bool, Depends(verify_api_key)], # noqa

        min_lat: float = Query(..., description="Широта первого угла прямоугольника"),
        max_lat: float = Query(..., description="Долгота второго угла прямоугольника"),
        min_lon: float = Query(..., description="Широта первого угла прямоугольника"),
        max_lon: float = Query(..., description="Долгота второго угла прямоугольника"),
):
    """
    Поиск организаций в указанной области
    :param request:
    :param min_lat:
    :param max_lat:
    :param min_lon:
    :param max_lon:

    :return: List[OrganizationResponse]
    """
    if authorized:
        return await organization_service.get_organizations_within_rectangle(
            min_lat,
            max_lat,
            min_lon,
            max_lon
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")



@router.get("/organizations/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
        organization_id: int,
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)], # noqa
        authorized: Annotated[bool, Depends(verify_api_key)], # noqa
):
    """
    Получить организацию по id

    :param organization_id:
    :return: OrganizationResponse
    """
    if authorized:
        return await organization_service.get_organization(organization_id)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
