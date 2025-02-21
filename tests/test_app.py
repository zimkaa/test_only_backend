import pytest
from litestar.testing import TestClient
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_index_route(client):
    """Тест корневого маршрута `/`."""
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Welcome</h1>" in response.text


def test_form_page(client):
    """Тест страницы формы `/form`."""
    response = client.get("/form")
    assert response.status_code == 200
    assert "<h1>Form Page</h1>" in response.text


def test_form_name_validation_error(client):
    """Тест валидации данных (пробела в имени)."""
    response = client.get(
        "/form", params={"date": "2025-03-10", "first_name": "John Doe", "last_name": "Smith"})
    assert response.status_code == 400
    assert '"first_name": ' in response.text


def test_form_date_validation_error(client):
    """Тест валидации данных (пробела в дате)."""
    response = client.get(
        "/form", params={"date": "2025-03-55", "first_name": "John Doe", "last_name": "Smith"})
    assert response.status_code == 400
    assert '"date": ' in response.text


def test_form_success(client):
    """Тест успешной обработки данных формы."""
    response = client.get(
        "/form", params={"first_name": "John", "last_name": "Smith", "date": "2025-03-10"})
    assert response.status_code == 200
    assert "John Smith" in response.text


def test_api_submit_success(client):
    """Тест успешного API-запроса `/api/submit`."""
    response = client.post(
        "/api/submit", json={"date": "2025-03-10", "first_name": "John", "last_name": "Smith"})
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["success"] is True
    assert 1 < len(json_data["data"]) < 6


def test_api_submit_validation_error(client):
    """Тест ошибки в API (неправильный формат даты)."""
    response = client.post(
        "/api/submit", json={"date": "invalid-date", "first_name": "John", "last_name": "Smith"})
    assert response.status_code == 400
    json_data = response.json()
    assert "date" in json_data["error"]


def test_api_submit_whitespace_error(client):
    """Тест ошибки в API (пробел в имени)."""
    response = client.post(
        "/api/submit", json={"date": "2025-03-10", "first_name": "John Doe", "last_name": "Smith"})
    assert response.status_code == 400
    json_data = response.json()
    assert "first_name" in json_data["error"]
