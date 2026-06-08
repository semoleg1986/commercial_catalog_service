from __future__ import annotations

import os

from fastapi.testclient import TestClient

from src.interface.http.app import create_app
from src.interface.http.wiring import reset_runtime_state


def _client() -> TestClient:
    os.environ["COMMERCIAL_CATALOG_USE_INMEMORY"] = "1"
    os.environ["COMMERCIAL_CATALOG_SERVICE_TOKEN"] = "test-service-token"
    reset_runtime_state()
    return TestClient(create_app())


def _service_headers(role: str = "admin") -> dict[str, str]:
    return {
        "X-Actor-Roles": role,
        "X-Actor-User-Id": f"{role}-user-1",
        "X-Service-Token": "test-service-token",
    }


def test_internal_course_offer_read_model_contract() -> None:
    client = _client()
    headers = _service_headers()

    upsert_response = client.post(
        "/internal/v1/course-offers",
        headers=headers,
        json={
            "offer_id": "course-1-standard",
            "course_id": "course-1",
            "offer_code": "standard",
            "title": "Standard",
            "description_short": "Standard access",
            "currency": "USD",
            "list_price": 100,
            "sale_price": 80,
            "is_active": True,
            "is_default": True,
        },
    )
    assert upsert_response.status_code == 201, upsert_response.text
    assert upsert_response.json()["description_short"] == "Standard access"
    assert upsert_response.json()["is_default"] is True

    list_response = client.get(
        "/internal/v1/courses/course-1/offers",
        headers=headers,
    )
    assert list_response.status_code == 200, list_response.text
    payload = list_response.json()
    assert payload["course_id"] == "course-1"
    assert payload["offers"][0]["offer_id"] == "course-1-standard"
    assert payload["offers"][0]["price"]["sale_price"] == 80

    status_response = client.get(
        "/internal/v1/courses/course-1/default-offer-status",
        headers=headers,
    )
    assert status_response.status_code == 200, status_response.text
    assert status_response.json() == {
        "course_id": "course-1",
        "has_active_default_offer": True,
    }


def test_internal_course_offer_read_model_requires_service_token() -> None:
    client = _client()

    response = client.get("/internal/v1/courses/course-1/offers")

    assert response.status_code == 401
    assert response.headers["content-type"] == "application/problem+json"


def test_internal_course_offer_write_requires_actor_context() -> None:
    client = _client()

    response = client.post(
        "/internal/v1/course-offers",
        headers={"X-Service-Token": "test-service-token"},
        json={
            "offer_id": "course-1-standard",
            "course_id": "course-1",
            "offer_code": "standard",
            "title": "Standard",
            "description_short": "Standard access",
            "currency": "USD",
            "list_price": 100,
            "sale_price": 80,
            "is_active": True,
            "is_default": True,
        },
    )

    assert response.status_code == 403
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["type"] == "https://api.example.com/problems/access-denied"


def test_internal_course_offer_write_rejects_non_admin_actor() -> None:
    client = _client()

    response = client.post(
        "/internal/v1/course-offers",
        headers=_service_headers("teacher"),
        json={
            "offer_id": "course-1-standard",
            "course_id": "course-1",
            "offer_code": "standard",
            "title": "Standard",
            "description_short": "Standard access",
            "currency": "USD",
            "list_price": 100,
            "sale_price": 80,
            "is_active": True,
            "is_default": True,
        },
    )

    assert response.status_code == 403
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["detail"] == "Изменение offer доступно только admin actor."
