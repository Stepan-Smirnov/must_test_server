import datetime as dt
from datetime import datetime
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.db import async_session_maker
from app.main import app
from app.models import Base, Data
from tests.config import settings
from tests.constants import TEST_DATA_COUNT

base_dir = Path(__file__).parent.parent

engine = create_async_engine(url=settings.TEST_DATABASE_URL)

async_session_maker.configure(bind=engine)


@pytest.fixture(scope="session", autouse=True)
async def setup_db() -> None:
    """Create Database"""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def session(request) -> AsyncSession:
    """Create async session"""

    async with async_session_maker() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()


@pytest.fixture
async def data_instance(session: AsyncSession) -> int:
    """Create data instance for test"""

    data_list = [
        Data(
            text=f"test_{i}",
            sequence_number=i,
            created_at=datetime.now(tz=dt.UTC),
        )
        for i in range(1, TEST_DATA_COUNT + 1)
    ]
    session.add_all(instances=data_list)
    await session.commit()
    yield len(data_list)
    await session.execute(delete(Data))
    await session.commit()


@pytest.fixture(scope="class")
async def client(request) -> AsyncClient:
    """Create async client"""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        request.cls.client: AsyncClient = client
        yield


@pytest.fixture
def test_data_obj() -> dict[str, str | int]:
    """Create test data object"""

    return dict(
        text="test_string",
        created_at=str(datetime.now(tz=dt.UTC)),
        sequence_number=1,
    )
