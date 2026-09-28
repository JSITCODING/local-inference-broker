import re

from local_inference_broker.models import RunRequest, TaskName
from local_inference_broker.providers.base import ProviderResult


class DeterministicProvider:
    """Small predictable provider for tests and connectivity checks."""

    async def run(self, request: RunRequest) -> ProviderResult:
        normalized = " ".join(request.input.split())
        if request.task is TaskName.SUMMARIZE:
            sentences = re.split(r"(?<=[.!?])\s+", normalized)
            output = " ".join(sentences[:2])[:600]
        elif request.task is TaskName.EXTRACT:
            items = [item.strip(" -\t") for item in request.input.splitlines() if item.strip()]
            selected = items[:20]
            output = "\n".join(selected)
            return ProviderResult(
                output=output,
                provider="deterministic",
                structured={"items": selected},
                warnings=("Deterministic extraction is a connectivity baseline, not semantic AI.",),
            )
        else:
            output = normalized

        return ProviderResult(
            output=output,
            provider="deterministic",
            warnings=("Deterministic output is intended for tests and connectivity checks.",),
        )

