import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import EXC_LOG_ERROR, MAX_ITEMS_PAGE, MIN_NUMBER_PAGE
from app.crud import data_crud
from app.db import get_async_session
from app.exception import ServerError
from app.schemes.data import CreateData, PaginateData, ReadData

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    path="",
    summary="Create data",
    response_model=ReadData,
    status_code=status.HTTP_200_OK,
)
async def create_data(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    data: CreateData,
):
    """
    - **text**: (str) text from 1 character to 32 characters
    - **created_at**: (datetime) current date and time of the received data
    - **sequence_number**: (int) ordinal number, a positive number
    """

    return await data_crud.create(obj_in=data, session=session)


@router.get(
    path="",
    summary="GetData",
    response_model=PaginateData,
    status_code=status.HTTP_200_OK,
)
async def get_data(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    page: Annotated[
        int, Query(ge=1, description="Номер страницы")
    ] = MIN_NUMBER_PAGE,
    per_page: Annotated[
        int, Query(ge=1, le=10, description="Кол-во элементов на странице")
    ] = MAX_ITEMS_PAGE,
):
    """
    - **page**: Query (int) - min = 1, default = 1, number of page
    - **per_page**: Query (int) - min 1, max = 10, default = 10, count object
    """

    try:
        data_list = await data_crud.get_all(
            session=session, offset=(page - 1) * per_page, limit=per_page
        )
        total_items = await data_crud.get_count(session=session)
        total_pages = (total_items + per_page - 1) // per_page
        return PaginateData(
            data=[
                ReadData.model_validate(data, from_attributes=True)
                for data in data_list
            ],
            current_page=page,
            per_page=per_page,
            total_items=total_items,
            total_pages=total_pages,
        )
    except Exception:
        logger.exception(msg=EXC_LOG_ERROR)
        raise ServerError
