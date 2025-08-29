from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.schemes.data import CreateData

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
        - **text**: текст от 1 символа, без пробелов
        - **created_at**: дата и время полученных данных
        - **sequence_number**: порядковый номер, положительное число
    """""

    print(data.created_at)
