import httpx
import pytest
from fastapi import status

from app.api.endpoints.data import get_data
from app.main import app
from app.schemes.data import PaginateData


@pytest.mark.usefixtures("client")
class TestDataEndpoint:
    """Test Class for data endpoints"""

    @staticmethod
    async def get_data(
        client: httpx.AsyncClient,
        **params: httpx.QueryParams,
    ):
        return await client.get(
            url=app.url_path_for(get_data.__name__), params=params
        )

    async def test_get_data(
        self,
        data_instance: int,
    ) -> None:
        """GET data objects"""

        response = await self.get_data(client=self.client)
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
            (3, 7, status.HTTP_200_OK),
            (1, 6, status.HTTP_200_OK),
            (2, 9, status.HTTP_200_OK),
            (4, 3, status.HTTP_200_OK),
        ],
        ids=[
            "1page_1obj",
            "2page_10obj",
            "3page_7obj",
            "1page_6obj",
            "2page_9obj",
            "4page_3obj",
        ],
    )
    async def test_data_with_query(
        self,
        data_instance: int,
        page: int,
        per_page: int,
        status_code: int,
    ) -> None:
        """Get object with good query"""

        response = await self.get_data(
            client=self.client, page=page, per_page=per_page
        )
        r_json: dict = response.json()
        r_page = r_json.get("current_page")
        r_per_page = r_json.get("per_page")
        r_data = r_json.get("data")
        total_items = r_json.get("total_items")
        assert response.status_code == status_code
        assert r_page == page
        assert r_per_page == per_page
        assert total_items == data_instance
        item_offset = (r_page - 1) * per_page
        assert len(r_data) == min(r_per_page, total_items - item_offset)

    @pytest.mark.parametrize(
        argnames="page",
        argvalues=[0, -1],
        ids=["zero_page", "negative_page"],
    )
    async def test_get_data_bad_page(
        self,
        page: int,
    ) -> None:
        """Get Objects with bad page query"""

        response = await self.get_data(client=self.client, page=page)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        argnames="per_page",
        argvalues=[0, -1, 11],
        ids=["zero_per_page", "negative_peg_page", "big_per_page"],
    )
    async def test_get_data_bad_per_page(
        self,
        per_page: int,
    ) -> None:
        """Get Objects with bad per_page query"""

        response = await self.get_data(client=self.client, per_page=per_page)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
