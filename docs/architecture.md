# Architecture and trust boundaries

## Purpose

Local Inference Broker gives clients one small contract for local inference work. It is a routing boundary, not an agent framework or privacy guarantee for every provider.

## Data flow

```text
client
  -> POST /v1/run
  -> validation and provider selection
  -> deterministic provider or local Ollama API
  -> typed response with measurements
```

The service generates an opaque request ID in memory. It does not intentionally persist request or response bodies.

## Provider behavior

- `deterministic` is a predictable test and connectivity baseline.
- `ollama` calls the configured Ollama HTTP endpoint.
- `auto` currently resolves to Ollama; it is not a fallback chain.

The deterministic provider does not claim semantic understanding. Ollama quality, storage, telemetry, model licensing, and hardware behavior remain properties of the installed Ollama environment and model.

## Network boundary

The default host is `127.0.0.1`. `localhost` and `::1` are also accepted as loopback. Any other host requires `LIB_BEARER_TOKEN`; API callers then send the same value as a bearer token. This is a guardrail, not a substitute for TLS or a hardened gateway.

`GET /health` intentionally remains unauthenticated and returns only service name, status, and version. `POST /v1/run` is authenticated when a token is configured.

## Failure model

- Provider timeout: HTTP 504 with a content-free error message.
- Provider unavailable: HTTP 503.
- Provider HTTP error: HTTP 502.
- Invalid input: FastAPI validation response.
- Invalid extracted JSON: successful response with a warning and no structured payload.

Error messages do not echo request content.

## Explicit non-goals

No public ingress, cloud provider, persistence, RAG, memory, agents, queue, frontend, or client-application integration belongs to v0.1.
