import logging
from typing import Any

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import EXC_LOG_ERROR
from app.exception import ServerError

logger = logging.getLogger(__name__)


class CrudBase[T]:
    def __init__(self, model):
        self.__model = model

    async def get_all(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        sort_by: str = "id",
        sort_desc: bool = False,
        **param: dict[str, Any],
    ) -> list[T]:
        """Get a list of objects"""

        sort_obj = getattr(self.__model, sort_by)

        if sort_desc:
            sort_obj = desc(sort_obj)

        query = (
            select(self.__model)
            .filter_by(**param)
            .order_by(sort_obj)
            .offset(offset)
            .limit(limit)
        )

        result = await session.scalars(query)
        return result.all()

    async def create(self, obj_in, session: AsyncSession) -> T:
        """Creating an object based on a Pydantic schema"""

        try:
            obj = self.__model(**obj_in.dict())
            session.add(obj)
            await session.commit()
            return obj
        except Exception:
            await session.rollback()
            logger.exception(msg=EXC_LOG_ERROR)
            raise ServerError

    async def get_count(self, session: AsyncSession) -> int:
        """Get the total number of object"""

        return await session.scalar(select(func.count(self.__model.id)))
