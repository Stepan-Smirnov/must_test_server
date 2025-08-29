from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import ServerError


class CrudBase:

    def __init__(self, model):
        self.__model = model

    async def get_all(self, session: AsyncSession, **param):

        """Возвращаем список объектов по заданным параметрам"""

        result = await session.scalars(select(self.__model).filter_by(**param))
        return result.all()

    async def create(self, obj_in, session: AsyncSession):

        """Создаем объект на основе Pydantic схемы"""
        try:
            obj = self.__model(**obj_in.dict())
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
        except Exception:
            await session.rollback()
            raise ServerError
