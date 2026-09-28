import pytest
from fastapi.testclient import TestClient

from local_inference_broker.api import create_app
from local_inference_broker.settings import Settings


def test_health_is_small_and_public() -> None:
    client = TestClient(create_app(Settings()))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "local-inference-broker"


def test_deterministic_run_returns_metrics_without_persisting_content() -> None:
    client = TestClient(create_app(Settings()))
    response = client.post(
        "/v1/run",
        json={
            "task": "summarize",
            "input": "First fact. Second fact. Third fact.",
            "provider": "deterministic",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["output"] == "First fact. Second fact."
    assert body["metrics"]["input_characters"] == 36
    assert body["provider"] == "deterministic"


def test_bearer_token_is_required_when_configured() -> None:
    client = TestClient(create_app(Settings(bearer_token="synthetic-test-token")))
    payload = {"task": "ask", "input": "hello", "provider": "deterministic"}
    assert client.post("/v1/run", json=payload).status_code == 401
    allowed = client.post(
        "/v1/run",
        json=payload,
        headers={"Authorization": "Bearer synthetic-test-token"},
    )
    assert allowed.status_code == 200


def test_incorrect_bearer_token_is_rejected() -> None:
    client = TestClient(create_app(Settings(bearer_token="synthetic-test-token")))
    response = client.post(
        "/v1/run",
        json={"task": "ask", "input": "synthetic", "provider": "deterministic"},
        headers={"Authorization": "Bearer incorrect-synthetic-token"},
    )
    assert response.status_code == 401


def test_unknown_request_fields_are_rejected() -> None:
    client = TestClient(create_app(Settings()))
    response = client.post(
        "/v1/run",
        json={
            "task": "ask",
            "input": "synthetic",
            "provider": "deterministic",
            "persist": True,
        },
    )
    assert response.status_code == 422


def test_lan_binding_without_token_is_rejected() -> None:
    with pytest.raises(ValueError, match="LAN binding requires"):
        create_app(Settings(host="0.0.0.0"))
