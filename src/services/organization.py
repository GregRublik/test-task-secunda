from typing import Union, List

from db.models import Organization
from repositories.base import SQLAlchemyRepository
from repositories.organization import OrganizationRepository
from sqlalchemy.ext.asyncio import AsyncSession

class OrganizationService:

    def __init__(
            self,
            repository: Union[SQLAlchemyRepository, OrganizationRepository],
            session: AsyncSession
    ):
        self.repository = repository
        self.session = session

    async def get_organization(self, organization_id: int) -> Organization:
        return await self.repository.find_one(self.session, {"id": organization_id})

    async def get_organizations(self, filters) -> List[Organization]:
        return await self.repository.find_all(self.session, filters)

    async def create_organization(self, organization_data: dict) -> Organization:
        return await self.repository.add_one(self.session, organization_data)

    async def update_organization(self, organization_data: dict) -> Organization:
        return await self.repository.change_one(self.session, organization_data)

    async def get_organizations_within_radius(self, latitude, longitude, radius_km):
        pass

