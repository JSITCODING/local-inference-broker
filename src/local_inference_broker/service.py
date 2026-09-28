from time import perf_counter
from uuid import uuid4

import httpx

from local_inference_broker.models import ProviderName, RunMetrics, RunRequest, RunResponse
from local_inference_broker.providers.base import Provider, ProviderResult
from local_inference_broker.providers.deterministic import DeterministicProvider
from local_inference_broker.providers.ollama import OllamaProvider
from local_inference_broker.settings import Settings


class BrokerError(RuntimeError):
    def __init__(self, code: str, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class BrokerService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def _provider(self, request: RunRequest) -> Provider:
        if request.provider is ProviderName.DETERMINISTIC:
            return DeterministicProvider()
        return OllamaProvider(self._settings)

    async def run(self, request: RunRequest) -> RunResponse:
        request_id = uuid4().hex
        started = perf_counter()
        try:
            result: ProviderResult = await self._provider(request).run(request)
        except httpx.TimeoutException as exc:
            raise BrokerError("provider_timeout", "The local provider timed out.", 504) from exc
        except httpx.HTTPStatusError as exc:
            raise BrokerError(
                "provider_http_error",
                "The local provider returned an error.",
            ) from exc
        except httpx.RequestError as exc:
            raise BrokerError(
                "provider_unavailable",
                "The local provider is unavailable.",
                503,
            ) from exc

        latency_ms = round((perf_counter() - started) * 1000)
        output_size = len(result.output)
        input_size = len(request.input)
        ratio = round(output_size / input_size, 4) if input_size else None
        return RunResponse(
            request_id=request_id,
            task=request.task,
            provider=result.provider,
            model=result.model,
            output=result.output,
            structured=result.structured,
            metrics=RunMetrics(
                input_characters=input_size,
                output_characters=output_size,
                latency_ms=latency_ms,
                compression_ratio=ratio,
            ),
            warnings=list(result.warnings),
        )
