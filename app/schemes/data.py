import datetime as dt
from datetime import datetime
from typing import Annotated

from pydantic import (
    AwareDatetime,
    BaseModel,
    Field,
    PastDatetime,
    PositiveInt,
    field_validator,
)

from app.constants import MAX_TEXT_LENGTH, MIN_TEXT_LENGTH
from app.exception import BadDatetime, TextSpace


class CreateData(BaseModel):
    """Валидация входных данных"""

    text: Annotated[
        str, Field(min_length=MIN_TEXT_LENGTH, max_length=MAX_TEXT_LENGTH)
    ]
    created_at: Annotated[datetime, AwareDatetime, PastDatetime]
    sequence_number: PositiveInt

    @field_validator("text", check_fields=False)
    def text_validator(cls, value: str):
        if value.isspace():
            raise TextSpace
        return value

    @field_validator("created_at", check_fields=False)
    def created_at_validator(cls, value: datetime):
        now = datetime.now(tz=dt.UTC)
        if value.year < now.year or (
            value.year == now.year and value.month < now.month
        ):
            raise BadDatetime
        return value


class ReadData(BaseModel):
    """Валидация входных данных"""

    id: int
    text: str
    created_at: datetime
    sequence_number: int


class PaginateData(BaseModel):
    """Вывод данных с пагинацией"""

    data: list[ReadData]
    current_page: int
    per_page: int
    total_items: int
    total_pages: int
