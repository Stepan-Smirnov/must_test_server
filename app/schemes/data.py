from typing import Annotated
from datetime import datetime

from pydantic import (
    BaseModel, Field, AwareDatetime, PastDatetime,
    PositiveInt, field_validator
)

from app.exception import TextSpace


class CreateData(BaseModel):

    """Валидация входных данных"""

    text: Annotated[str, Field(min_length=1)]
    created_at: Annotated[datetime, AwareDatetime(), PastDatetime()]
    sequence_number: PositiveInt

    @field_validator('text', check_fields=False)
    def text_validator(cls, value: str):
        if value.isspace():
            raise TextSpace
        return value


class ReadData(CreateData):

    """Валидация данных при отправке"""

    id: PositiveInt