from dataclasses import dataclass
from typing import Any, Protocol

from local_inference_broker.models import RunRequest


@dataclass(frozen=True)
class ProviderResult:
    output: str
    provider: str
    model: str | None = None
    structured: dict[str, Any] | list[Any] | None = None
    warnings: tuple[str, ...] = ()


class Provider(Protocol):
    async def run(self, request: RunRequest) -> ProviderResult: ...

