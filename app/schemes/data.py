from typing import Annotated
from datetime import datetime, timezone

from pydantic import (
    BaseModel, Field, AwareDatetime, PastDatetime,
    PositiveInt, field_validator
)

from app.exception import TextSpace, BadDatetime
from constants import MIN_TEXT_LENGTH, MAX_TEXT_LENGTH


class CreateData(BaseModel):

    """Валидация входных данных"""

    text: Annotated[
        str, Field(min_length=MIN_TEXT_LENGTH, max_length=MAX_TEXT_LENGTH)
    ]
    created_at: Annotated[datetime, AwareDatetime, PastDatetime]
    sequence_number: PositiveInt

    @field_validator('text', check_fields=False)
    def text_validator(cls, value: str):
        if value.isspace():
            raise TextSpace
        return value

    @field_validator('created_at', check_fields=False)
    def created_at_validator(cls, value: datetime):
        now = datetime.now(tz=timezone.utc)
        if value.year < now.year or (
            value.year == now.year and value.month < now.month
        ):
            raise BadDatetime
        return value
