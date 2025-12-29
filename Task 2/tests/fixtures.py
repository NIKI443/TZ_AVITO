import pytest
import requests
from tests.schemas import AdvertisementCreateResponse

BASE_URL = "https://qa-internship.avito.com"
DEFAULT_SELLER_ID = 80000


@pytest.fixture()
def new_advertisement() -> AdvertisementCreateResponse:
    url = f"{BASE_URL}/api/1/item"
    body = {
        "sellerID": DEFAULT_SELLER_ID,
        "name": "test_advertisement",
        "price": 100,
        "statistics": {
            "likes": 10,
            "viewCount": 230,
            "contacts": 25
        }
    }
    response = requests.post(url, json=body)
    return AdvertisementCreateResponse.model_validate(response.json())
