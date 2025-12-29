# Автотесты для микросервиса объявлений Avito  

Данный репозиторий содержит:
- оформленные вручную тест-кейсы (`TESTCASES.md`)
- комплект автотестов на `pytest` для проверки API
- инструкцию по запуску и установке окружения
- примеры фактического поведения API

---

- `requirements.md` — библиотеки для автотестов  
- `conftest.py` — фикстуры (session, base_url, seller_id, created_item)  
- `test_items_api.py` — сами автотесты  
- `TESTCASES.md` — ручные тест-кейсы 

## Запуск автотестов в IDE
- Клонировать репозиторий и перейти в дирректорию
```
git clone <repository-url>
cd <repository-directory>
```
- Создать виртуальное окружение (для windows)
```
python -m venv venv
venv\Scripts\activate
```
- Скачать необходимые библиотеки
```
pip install -r requirements.txt
```
- Запустить автотесты из корневого репозитория
```
pytest -v
```

