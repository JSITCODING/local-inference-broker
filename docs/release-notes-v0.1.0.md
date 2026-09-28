# Local Inference Broker v0.1.0

Local Inference Broker introduces a small, local-first routing boundary for `ask`, `summarize`, and `extract` tasks.

## Included

- Typed FastAPI request and response contract.
- `local-ai` command-line client and server command.
- Deterministic provider for repeatable tests.
- Optional integration with a locally running Ollama API.
- Provider identity, latency, character counts, and measured compression ratio.
- Loopback default and bearer-token requirement for non-loopback binding.

## Boundaries

This is a prototype release. It does not persist prompts, provide a public service, guarantee model quality, or include agents, memory, RAG, a frontend, or cloud providers. All repository examples are synthetic.

## Verification

The release requires passing tests, Ruff, strict mypy, package build, CLI smoke test, secret scanning, and privacy-path scanning on Python 3.11–3.13 where applicable.
