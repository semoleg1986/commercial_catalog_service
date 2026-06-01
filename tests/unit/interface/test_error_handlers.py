from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from src.interface.http.errors import register_exception_handlers


def test_http_error_response_contains_trace_ids() -> None:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/internal-only")
    def internal_only() -> None:
        raise HTTPException(status_code=401, detail="Требуется X-Service-Token.")

    client = TestClient(app)
    response = client.get(
        "/internal-only",
        headers={
            "X-Request-ID": "req-catalog-001",
            "X-Correlation-ID": "corr-catalog-001",
        },
    )

    assert response.status_code == 401
    assert response.headers.get("content-type") == "application/problem+json"
    assert response.headers.get("X-Request-ID") == "req-catalog-001"
    assert response.headers.get("X-Correlation-ID") == "corr-catalog-001"
    assert (
        response.json().get("type") == "https://api.example.com/problems/unauthorized"
    )
    assert response.json().get("status") == 401
    assert response.json().get("detail") == "Требуется X-Service-Token."
    assert response.json().get("request_id") == "req-catalog-001"
    assert response.json().get("correlation_id") == "corr-catalog-001"
