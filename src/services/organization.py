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

    async def get_organization(self, data) -> Organization:
        return await self.repository.find_one(self.session, data)

    async def get_organizations(self, data) -> List[Organization]:
        return await self.repository.find_all(self.session, data)
