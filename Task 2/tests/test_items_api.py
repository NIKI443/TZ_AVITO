# tests/test_items_api.py

def test_create_item_success(session, base_url, seller_id):
    payload = {
        "sellerId": seller_id,
        "name": "Тестовое объявление",
        "price": 1000,
        "statistics": {
            "likes": 10,
            "viewCount": 20,
            "contacts": 30,
        },
    }

    resp = session.post(f"{base_url}/api/1/item", json=payload)

    assert resp.status_code == 200
    body = resp.json()
    assert "status" in body
    assert "Сохранили объявление -" in body["status"]


def test_get_item_by_id_returns_created_item(session, base_url, created_item):
    item_id = created_item["id"]

    resp = session.get(f"{base_url}/api/1/item/{item_id}")

    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    item = data[0]
    assert item["id"] == item_id
    assert item["sellerId"] == created_item["sellerId"]
    assert item["name"] == created_item["payload"]["name"]
    assert item["price"] == created_item["payload"]["price"]
    assert "statistics" in item
    assert isinstance(item["statistics"], dict)


def test_get_items_by_seller_returns_created_item(session, base_url, created_item):
    seller_id = created_item["sellerId"]

    resp = session.get(f"{base_url}/api/1/{seller_id}/item")

    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    ids = {item["id"] for item in data}
    assert created_item["id"] in ids


def test_get_statistics_for_item(session, base_url, created_item):
    item_id = created_item["id"]

    resp = session.get(f"{base_url}/api/1/statistic/{item_id}")

    assert resp.status_code == 200

    stats = resp.json()


    if isinstance(stats, list):
        assert len(stats) >= 1, "Ожидали хотя бы один элемент статистики"
        stats = stats[0]

    for key in ("likes", "viewCount", "contacts"):
        assert key in stats, f"В статистике нет поля {key}"
        assert isinstance(stats[key], int), f"Поле {key} должно быть числом"
def test_delete_item_success(session, base_url, created_item):
    """Тест успешного удаления объявления"""
    item_id = created_item["id"]

    resp = session.delete(f"{base_url}/api/2/item/{item_id}")

    assert resp.status_code == 200
    
    assert resp.text == "" or "Удалили" in resp.text

    get_resp = session.get(f"{base_url}/api/1/item/{item_id}")
    assert get_resp.status_code == 404

def test_create_item_without_statistics_returns_error(session, base_url, seller_id):
    """Тест создания объявления без обязательных полей statistics"""
    payload = {
        "sellerId": seller_id,
        "name": "Объявление без статистики",
        "price": 2000,
    }

    resp = session.post(f"{base_url}/api/1/item", json=payload)

    assert resp.status_code == 400
    
    body = resp.json()
    assert "status" in body
    assert "400" in body["status"]
    assert "result" in body
    assert "message" in body["result"]
    assert "обязательно" in body["result"]["message"].lower()
