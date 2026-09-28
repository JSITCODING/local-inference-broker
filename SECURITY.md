# Security policy

Local Inference Broker is an experimental, local-first prototype. Supported security updates apply to the latest tagged `0.1.x` release.

## Security properties

- Loopback is the default network boundary.
- Non-loopback listening requires an explicit bearer token.
- Providers remain local unless a future provider is separately reviewed and approved.
- Request and response bodies are not persisted or logged.
- Repository tests and examples contain synthetic material only.

## Unsupported deployments

- Direct exposure to the public internet.
- Non-loopback use without TLS supplied by a separately reviewed trusted network layer.
- Reusing bearer tokens in repositories, examples, shell profiles, or issue reports.
- Assuming a provider has the same privacy boundary as the broker without reviewing that provider.

## Reporting

Do not open a public issue for a vulnerability. Contact the repository owner privately with the affected version, reproduction steps, impact, and any suggested mitigation. Do not include real prompt content or credentials.

Do not place credentials in issues, logs, examples, command history, or Git.
