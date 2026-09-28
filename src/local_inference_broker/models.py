from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TaskName(StrEnum):
    ASK = "ask"
    SUMMARIZE = "summarize"
    EXTRACT = "extract"


class ProviderName(StrEnum):
    AUTO = "auto"
    DETERMINISTIC = "deterministic"
    OLLAMA = "ollama"


class RunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task: TaskName = TaskName.ASK
    input: str = Field(min_length=1, max_length=200_000)
    provider: ProviderName = ProviderName.AUTO
    model: str | None = Field(default=None, max_length=120)
    timeout_seconds: float = Field(default=30.0, ge=1.0, le=300.0)


class RunMetrics(BaseModel):
    input_characters: int
    output_characters: int
    latency_ms: int
    compression_ratio: float | None = None


class RunResponse(BaseModel):
    request_id: str
    status: str = "ok"
    task: TaskName
    provider: str
    model: str | None
    output: str
    structured: dict[str, Any] | list[Any] | None = None
    metrics: RunMetrics
    warnings: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "local-inference-broker"
    version: str

