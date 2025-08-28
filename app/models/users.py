from sqlalchemy import DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Data(Base):

    __tablename__ = 'data'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    text: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    sequence_number: Mapped[int] = mapped_column(BigInteger())