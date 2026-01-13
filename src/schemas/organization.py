from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from schemas.building import BuildingResponse
from schemas.activity import ActivityResponse


class OrganizationBase(BaseModel):
    name: str
    building_id: int
    phone_numbers: List[str] = Field(default_factory=list)


class OrganizationCreate(OrganizationBase):
    activity_ids: List[int] = []



class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    building_id: Optional[int] = None
    phone_numbers: Optional[List[str]] = None
    activity_ids: Optional[List[int]] = None



class OrganizationResponse(BaseModel):
    id: int
    name: str
    building_id: int
    phone_numbers: List[str]
    building: BuildingResponse
    activities: List[ActivityResponse]

    model_config = ConfigDict(from_attributes=True)


# Специальные схемы для запросов
class CoordinateRequest(BaseModel):
    latitude: float
    longitude: float


class RadiusSearchRequest(CoordinateRequest):
    radius_km: float = Field(gt=0, description="Радиус в километрах")


class RectangleSearchRequest(BaseModel):
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float


class OrganizationSearchRequest(BaseModel):
    name: Optional[str] = None
    activity_id: Optional[int] = None
    building_id: Optional[int] = None
