import os
from uuid import UUID
import requests
from tests.schemas import AdvertisementListResponse

BASE_URL = os.getenv("BASE_URL")
DEFAULT_SELLER_ID = os.getenv("DEFAULT_SELLER_ID")


def clear_seller_advertisements(seller_id: int=DEFAULT_SELLER_ID) -> None:
    response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
    ads = AdvertisementListResponse(advertisements=response.json())
    for ad in ads.advertisements:
        delete_advertisement(ad.id)


def delete_advertisement(_id: UUID) -> None:
    url = f"{BASE_URL}/api/2/item/{_id}"
    response = requests.delete(url)
    assert response.status_code == 200
