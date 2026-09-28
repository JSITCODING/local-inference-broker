import hmac
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from local_inference_broker import __version__
from local_inference_broker.models import HealthResponse, RunRequest, RunResponse
from local_inference_broker.service import BrokerError, BrokerService
from local_inference_broker.settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or Settings.from_env()
    resolved.validate_network_boundary()
    service = BrokerService(resolved)
    app = FastAPI(title="Local Inference Broker", version=__version__)

    async def authorize(authorization: Annotated[str | None, Header()] = None) -> None:
        if resolved.bearer_token is None:
            return
        expected = f"Bearer {resolved.bearer_token}"
        if authorization is None or not hmac.compare_digest(authorization, expected):
            raise HTTPException(
                status_code=401,
                detail={"code": "unauthorized", "message": "Invalid token."},
            )

    @app.exception_handler(BrokerError)
    async def broker_error_handler(_request: object, exc: BrokerError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": {"code": exc.code, "message": str(exc)}},
        )

    @app.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(version=__version__)

    @app.post("/v1/run", response_model=RunResponse, dependencies=[Depends(authorize)])
    async def run(request: RunRequest) -> RunResponse:
        return await service.run(request)

    return app


app = create_app()
