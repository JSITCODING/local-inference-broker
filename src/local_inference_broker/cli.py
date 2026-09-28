import json
import os
from typing import Annotated

import httpx
import typer
import uvicorn

from local_inference_broker.models import ProviderName, RunRequest, TaskName
from local_inference_broker.settings import Settings

app = typer.Typer(
    help="Send small inference tasks to a private local broker.",
    no_args_is_help=True,
)


def _request(
    task: TaskName,
    text: str,
    provider: ProviderName,
    model: str | None,
    url: str,
) -> None:
    payload = RunRequest(task=task, input=text, provider=provider, model=model)
    token = os.getenv("LOCAL_AI_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = httpx.post(
            f"{url.rstrip('/')}/v1/run",
            json=payload.model_dump(mode="json"),
            headers=headers,
            timeout=payload.timeout_seconds,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(response.json(), ensure_ascii=False, indent=2))


@app.command()
def ask(
    text: Annotated[str, typer.Argument(help="The request to send.")],
    provider: ProviderName = ProviderName.AUTO,
    model: str | None = None,
    url: str = "http://127.0.0.1:8787",
) -> None:
    _request(TaskName.ASK, text, provider, model, url)


@app.command()
def summarize(
    text: Annotated[str, typer.Argument(help="Text to summarize.")],
    provider: ProviderName = ProviderName.AUTO,
    model: str | None = None,
    url: str = "http://127.0.0.1:8787",
) -> None:
    _request(TaskName.SUMMARIZE, text, provider, model, url)


@app.command()
def extract(
    text: Annotated[str, typer.Argument(help="Text to extract structured facts from.")],
    provider: ProviderName = ProviderName.AUTO,
    model: str | None = None,
    url: str = "http://127.0.0.1:8787",
) -> None:
    _request(TaskName.EXTRACT, text, provider, model, url)


@app.command()
def serve() -> None:
    settings = Settings.from_env()
    settings.validate_network_boundary()
    uvicorn.run(
        "local_inference_broker.api:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
    )
