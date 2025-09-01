import pytest
from fastapi import status
from httpx import AsyncClient

from app.api.endpoints.data import get_data
from app.main import app
from app.schemes.data import PaginateData


async def test_get_data(client: AsyncClient, data_instance: int):
    """GET data objects"""

    response = await client.get(url=app.url_path_for(get_data.__name__))
    r_json: dict = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert PaginateData(**r_json)
    assert r_json.get("total_items") == data_instance
    assert r_json.get("current_page") == 1
    assert r_json.get("per_page") == 10


@pytest.mark.parametrize(
    argnames=("page", "per_page", "status_code"),
    argvalues=[
        (1, 1, status.HTTP_200_OK),
        (2, 10, status.HTTP_200_OK),
        (0, 10, status.HTTP_422_UNPROCESSABLE_ENTITY),
        (1, 11, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
    ids=["good", "good", "bad_page", "bad_per_page"],
)
async def test_data_with_query(
    client: AsyncClient,
    page: int,
    per_page: int,
    status_code: int,
):
    response = await client.get(
        url=app.url_path_for(get_data.__name__),
        params=dict(page=page, per_page=per_page),
    )
    assert response.status_code == status_code
