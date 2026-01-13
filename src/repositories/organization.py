from repositories.base import SQLAlchemyRepository
from db.models import Organization

class OrganizationRepository(SQLAlchemyRepository):
    model = Organization
