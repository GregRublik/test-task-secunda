from typing import Union, List

from db.models import Organization
from repositories.base import SQLAlchemyRepository
from repositories.organization import OrganizationRepository
from repositories.activity import ActivityRepository
from sqlalchemy.ext.asyncio import AsyncSession

class OrganizationService:

    def __init__(
            self,
            repository: Union[SQLAlchemyRepository, OrganizationRepository],
            activity_repository: Union[SQLAlchemyRepository, ActivityRepository],
            session: AsyncSession
    ):
        self.repository = repository
        self.session = session
        self.activity_repository = activity_repository

    async def get_organizations(self, filters):
        include_subactivities = filters.pop("include_subactivities", False)
        # обычный поиск
        if not include_subactivities or "activity_id" not in filters:
            return await self.repository.find_all(self.session, filters)
        # 🔥 поиск по поддереву
        activity_id = filters.pop("activity_id")
        activity_ids = await self.activity_repository.get_activity_subtree_ids(
            self.session,
            activity_id,
        )
        return await self.repository.find_by_activity_ids(
            self.session,
            activity_ids,
        )

    async def get_organization(self, organization_id: int) -> Organization:
        return await self.repository.get_by_id(self.session, organization_id)


    async def create_organization(self, organization_data: dict) -> Organization:

        activity_ids = organization_data.pop("activity_ids")

        return await self.repository.add_one(self.session, organization_data)

    async def update_organization(self, organization_data: dict) -> Organization:
        return await self.repository.change_one(self.session, organization_data)

    async def get_organizations_within_radius(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
    ):
        return await self.repository.find_within_radius(
            self.session,
            latitude,
            longitude,
            radius_km,
        )

    async def get_organizations_within_rectangle(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
    ):
        return await self.repository.find_within_rectangle(
            self.session,
            min_lat,
            max_lat,
            min_lon,
            max_lon,
        )

