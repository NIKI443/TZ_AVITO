import os
import uuid
import pytest
from tests.schemas import AdvertisementCreateResponse, AdvertisementStatisticsResponse, AdvertisementListResponse
import requests
from tests.utils import delete_advertisement

BASE_URL = os.getenv("BASE_URL")
DEFAULT_SELLER_ID = int(os.getenv("DEFAULT_SELLER_ID"))


class TestAdvertisementMicroservice:
    @pytest.mark.parametrize(
        "name, price, expected",
        [
            ("test-advertisement", 2000, 200),
            (False, 2000, 400),
            ("test-advertisement", False, 400),
        ]
    )
    def test_create_advertisement(self, name, price, expected):
        body = {
            "sellerID": DEFAULT_SELLER_ID,
            "name": name,
            "price": price,
            "statistics": {
                "likes": 10,
                "viewCount": 230,
                "contacts": 25
            }
        }
        response = requests.post(f"{BASE_URL}/api/1/item", json=body)
        assert response.status_code == expected

        if expected == 200:
            data: dict = response.json()
            advertisement = AdvertisementCreateResponse.model_validate(data)
            delete_advertisement(advertisement.get_uuid())


    @pytest.mark.parametrize(
        "_id, expected",
        [
            (uuid.uuid4(), 200),
            (uuid.uuid4(), 404),
            (False, 400),
        ]
    )
    def test_get_advertisement_by_id(self, _id, expected, new_advertisement: AdvertisementCreateResponse):
        if expected == 200:
            _id = new_advertisement.get_uuid()

        response = requests.get(f"{BASE_URL}/api/1/item/{_id}")
        assert response.status_code == expected

        if expected == 200:
            assert AdvertisementListResponse(advertisements=response.json())

        delete_advertisement(new_advertisement.get_uuid())


    @pytest.mark.parametrize(
        "_id, expected",
        [
            (DEFAULT_SELLER_ID, 200),
            (False, 400),
        ]
    )
    def test_get_advertisement_by_seller_id(self, _id, expected):
        response = requests.get(f"{BASE_URL}/api/1/{_id}/item")
        assert response.status_code == expected

        if expected == 200:
            assert AdvertisementListResponse(advertisements=response.json())


    @pytest.mark.parametrize(
        "_id, expected",
        [
            (DEFAULT_SELLER_ID, 200),
            (uuid.uuid4(), 404),
        ]
    )
    def test_get_advertisement_statistics(self, _id, expected, new_advertisement: AdvertisementCreateResponse):
        if expected == 200:
            _id = new_advertisement.get_uuid()

        response = requests.get(f"{BASE_URL}/api/2/statistic/{_id}")
        assert response.status_code == expected

        if expected == 200:
            assert AdvertisementStatisticsResponse(ad_statistics=response.json())

        delete_advertisement(new_advertisement.get_uuid())
