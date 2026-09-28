# Contributing

Local Inference Broker accepts small, reviewable changes that preserve its local-first boundary.

## Development setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Required checks

```bash
ruff check .
mypy src tests
pytest
python -m build
local-ai --help
```

Run `git diff --check` and a secret scan before proposing a change.

## Repository rules

- Use only synthetic fixtures and examples.
- Never commit prompts, transcripts, recordings, credentials, host details, or application data.
- Keep providers behind the typed request and response contract.
- Treat any new network destination or persistence mechanism as a security-boundary change.
- Document measured results as measurements, including the hardware and model context.

## Pull requests

Explain the problem, the smallest useful change, the checks run, and any privacy or network-boundary impact. A passing test suite does not by itself approve a new provider or public-network deployment.
