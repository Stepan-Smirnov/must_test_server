import datetime as dt
from datetime import datetime
from typing import Annotated

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    PastDatetime,
    PositiveInt,
    field_validator,
)

from app.constants import MAX_TEXT_LENGTH, MIN_TEXT_LENGTH
from app.exception import BadDatetime


class CreateData(BaseModel):
    """Validation of input data"""

    text: Annotated[
        str, Field(min_length=MIN_TEXT_LENGTH, max_length=MAX_TEXT_LENGTH)
    ]
    created_at: Annotated[datetime, AwareDatetime, PastDatetime]
    sequence_number: PositiveInt

    @field_validator("created_at", check_fields=False)
    def created_at_validator(cls, value: datetime):
        now = datetime.now(tz=dt.UTC)
        if value.year < now.year or (
            value.year == now.year and value.month < now.month
        ):
            raise BadDatetime
        return value

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class ReadData(BaseModel):
    """Validation of returned data"""

    id: int
    text: str
    created_at: datetime
    sequence_number: int


class PaginateData(BaseModel):
    """Data return with pagination"""

    data: list[ReadData]
    current_page: int
    per_page: int
    total_items: int
    total_pages: int
