from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Activity
from repositories.base import SQLAlchemyRepository


class ActivityRepository(SQLAlchemyRepository):

    async def get_activity_subtree_ids(
        self,
        session: AsyncSession,
        root_activity_id: int,
    ) -> list[int]:
        """
        Возвращает список id: [root, child1, child2, ...]
        """
        result_ids = []
        stack = [root_activity_id]

        while stack:
            current_id = stack.pop()
            result_ids.append(current_id)

            stmt = select(Activity.id).where(Activity.parent_id == current_id)
            res = await session.execute(stmt)
            children_ids = [row[0] for row in res.all()]

            stack.extend(children_ids)

        return result_ids
