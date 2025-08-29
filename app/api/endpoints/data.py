import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import data_crud
from app.db import get_async_session
from app.schemes.data import CreateData, ReadData
from app.exception import ServerError
from constants import EXC_LOG_ERROR, MIN_NUMBER_PAGE, MAX_ITEMS_PAGE

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    path='/',
    summary='Сохранение данных',
    response_model=ReadData
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


@router.get(
    path='/',
    summary="Получение данных",
    response_model=list[ReadData]
)
async def get_data(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        page: Annotated[
            int, Query(ge=1, description="Номер страницы")
        ] = MIN_NUMBER_PAGE,
        per_page: Annotated[
            int, Query(ge=1, le=10, description="Кол-во элементов на странице")
        ] = MAX_ITEMS_PAGE
):
    try:
        return await data_crud.get_all(
            session=session, offset=(page - 1) * per_page, limit=per_page
        )
    except Exception:
        logger.exception(msg=EXC_LOG_ERROR)
        raise ServerError
