# tests/conftest.py
import os
import random
import uuid

import pytest
import requests


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("API_BASE_URL", "https://qa-internship.avito.com")


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update(
        {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )
    return s


def is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except (ValueError, TypeError):
        return False


def extract_id_from_status(status: str) -> str:
    parts = status.split(" - ", maxsplit=1)
    if len(parts) != 2:
        raise ValueError(f"Неожиданный формат status: {status!r}")
    return parts[1].strip()


@pytest.fixture
def seller_id() -> int:
    return random.randint(111111, 999999)


@pytest.fixture
def created_item(session, base_url, seller_id):
    payload = {
        "sellerId": seller_id,
        "name": "Автотестовое объявление",
        "price": 1000,
        "statistics": {
            "likes": 1,
            "viewCount": 2,
            "contacts": 3,
        },
    }

    resp = session.post(f"{base_url}/api/1/item", json=payload)

    assert resp.status_code == 200, f"Ожидали 200 при создании, а получили {resp.status_code}"
    body = resp.json()
    assert "status" in body, "В ответе на создание нет поля 'status'"
    assert "Сохранили объявление -" in body["status"], "Статус не содержит ожидаемого текста"

    item_id = extract_id_from_status(body["status"])
    assert is_uuid(item_id), f"ID из статуса не похож на UUID: {item_id}"

    return {
        "id": item_id,
        "sellerId": seller_id,
        "payload": payload,
    }
