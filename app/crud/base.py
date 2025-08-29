import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import ServerError
from constants import EXC_LOG_ERROR

logger = logging.getLogger(__name__)


class CrudBase:

    def __init__(self, model):
        self.__model = model

    async def get_all(
            self,
            session: AsyncSession,
            sort_by: str = "id",
            **param
    ):

        """Возвращаем список объектов по заданным параметрам"""

        query = select(self.__model).filter_by(**param).order_by(
            getattr(self.__model, sort_by)
        )

        result = await session.scalars(query)
        return result.all()

    async def create(self, obj_in, session: AsyncSession):

        """Создаем объект на основе Pydantic схемы"""
        try:
            obj = self.__model(**obj_in.dict())
            session.add(obj)
            await session.commit()
            return obj
        except Exception:
            await session.rollback()
            logger.exception(msg=EXC_LOG_ERROR)
            raise ServerError
