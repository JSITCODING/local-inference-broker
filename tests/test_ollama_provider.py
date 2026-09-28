from typing import Any

import httpx
import pytest

from local_inference_broker.models import ProviderName, RunRequest, TaskName
from local_inference_broker.providers.ollama import OllamaProvider
from local_inference_broker.settings import Settings


@pytest.mark.asyncio
async def test_extract_parses_structured_json(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_post(
        _self: httpx.AsyncClient,
        url: str,
        **_kwargs: Any,
    ) -> httpx.Response:
        request = httpx.Request("POST", url)
        return httpx.Response(
            200,
            request=request,
            json={"response": '{"items": ["synthetic"]}'},
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    request = RunRequest(
        task=TaskName.EXTRACT,
        input="Synthetic item",
        provider=ProviderName.OLLAMA,
    )
    result = await OllamaProvider(Settings()).run(request)
    assert result.structured == {"items": ["synthetic"]}
    assert result.warnings == ()


@pytest.mark.asyncio
async def test_extract_warns_on_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_post(
        _self: httpx.AsyncClient,
        url: str,
        **_kwargs: Any,
    ) -> httpx.Response:
        request = httpx.Request("POST", url)
        return httpx.Response(200, request=request, json={"response": "not-json"})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    request = RunRequest(
        task=TaskName.EXTRACT,
        input="Synthetic item",
        provider=ProviderName.OLLAMA,
    )
    result = await OllamaProvider(Settings()).run(request)
    assert result.structured is None
    assert result.warnings == ("The provider response was not valid JSON.",)
