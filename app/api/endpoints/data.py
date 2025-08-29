import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.schemes.data import CreateData
from app.crud import data_crud


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    path='/',
    summary='Сохранение данных',
)
async def create_data(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        data: CreateData
):
    """
        - **text**: (str) текст от 1 символа до 32
        - **created_at**: (datetime) текущая дата и время полученных данных
        - **sequence_number**: (int) порядковый номер, положительное число
    """""
    return await data_crud.create(obj_in=data, session=session)

