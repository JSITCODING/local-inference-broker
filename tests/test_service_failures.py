import httpx
import pytest

from local_inference_broker.models import ProviderName, RunRequest
from local_inference_broker.providers.base import ProviderResult
from local_inference_broker.service import BrokerError, BrokerService
from local_inference_broker.settings import Settings


class TimeoutProvider:
    async def run(self, _request: RunRequest) -> ProviderResult:
        raise httpx.TimeoutException("synthetic timeout")


class UnavailableProvider:
    async def run(self, _request: RunRequest) -> ProviderResult:
        raise httpx.ConnectError("synthetic unavailable")


@pytest.mark.asyncio
async def test_timeout_becomes_content_free_gateway_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = BrokerService(Settings())
    monkeypatch.setattr(service, "_provider", lambda _request: TimeoutProvider())
    request = RunRequest(input="synthetic", provider=ProviderName.DETERMINISTIC)
    with pytest.raises(BrokerError) as raised:
        await service.run(request)
    assert raised.value.code == "provider_timeout"
    assert raised.value.status_code == 504
    assert "synthetic" not in str(raised.value)


@pytest.mark.asyncio
async def test_unavailable_provider_becomes_service_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = BrokerService(Settings())
    monkeypatch.setattr(service, "_provider", lambda _request: UnavailableProvider())
    request = RunRequest(input="synthetic", provider=ProviderName.DETERMINISTIC)
    with pytest.raises(BrokerError) as raised:
        await service.run(request)
    assert raised.value.code == "provider_unavailable"
    assert raised.value.status_code == 503
