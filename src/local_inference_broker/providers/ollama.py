import json

import httpx

from local_inference_broker.models import RunRequest, TaskName
from local_inference_broker.providers.base import ProviderResult
from local_inference_broker.settings import Settings

SYSTEM_PROMPTS = {
    TaskName.ASK: "Answer the request directly. Return concise plain text.",
    TaskName.SUMMARIZE: "Summarize the input faithfully and concisely. Do not add facts.",
    TaskName.EXTRACT: (
        "Extract the key entities and facts. Return valid JSON with an items array. "
        "Do not add facts that are not present."
    ),
}


class OllamaProvider:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def run(self, request: RunRequest) -> ProviderResult:
        model = request.model or self._settings.ollama_model
        payload = {
            "model": model,
            "prompt": request.input,
            "system": SYSTEM_PROMPTS[request.task],
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=request.timeout_seconds) as client:
            response = await client.post(
                f"{self._settings.ollama_url.rstrip('/')}/api/generate",
                json=payload,
            )
            response.raise_for_status()
        body = response.json()
        output = str(body.get("response", "")).strip()
        structured = None
        warnings: tuple[str, ...] = ()
        if request.task is TaskName.EXTRACT:
            try:
                parsed = json.loads(output)
                structured = parsed if isinstance(parsed, (dict, list)) else None
            except json.JSONDecodeError:
                warnings = ("The provider response was not valid JSON.",)
        return ProviderResult(
            output=output,
            provider="ollama",
            model=model,
            structured=structured,
            warnings=warnings,
        )
