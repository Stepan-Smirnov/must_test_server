from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from constants import DATABASE_URL

Base = declarative_base()

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():

    async with async_session_maker() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()