from datetime import datetime

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from constants import MAX_TEXT_LENGTH


class Data(Base):

    __tablename__ = 'data'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    text: Mapped[str] = mapped_column(String(length=MAX_TEXT_LENGTH))
    created_at: Mapped[datetime]
    sequence_number: Mapped[int] = mapped_column(BigInteger())