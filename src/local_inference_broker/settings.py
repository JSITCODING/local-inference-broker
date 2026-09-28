import ipaddress
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    host: str = "127.0.0.1"
    port: int = 8787
    bearer_token: str | None = None
    ollama_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:7b"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            host=os.getenv("LIB_HOST", "127.0.0.1"),
            port=int(os.getenv("LIB_PORT", "8787")),
            bearer_token=os.getenv("LIB_BEARER_TOKEN") or None,
            ollama_url=os.getenv("LIB_OLLAMA_URL", "http://127.0.0.1:11434"),
            ollama_model=os.getenv("LIB_OLLAMA_MODEL", "qwen2.5:7b"),
        )

    def validate_network_boundary(self) -> None:
        try:
            address = ipaddress.ip_address(self.host)
        except ValueError:
            is_loopback = self.host == "localhost"
        else:
            is_loopback = address.is_loopback

        if not is_loopback and not self.bearer_token:
            raise ValueError(
                "LAN binding requires LIB_BEARER_TOKEN. "
                "The broker never exposes an unauthenticated non-loopback listener."
            )
