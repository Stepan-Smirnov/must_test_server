from typing import Annotated
from datetime import datetime

from pydantic import (
    BaseModel, Field, AwareDatetime, PastDatetime,
    PositiveInt, field_validator
)

from app.exception import TextSpace
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
