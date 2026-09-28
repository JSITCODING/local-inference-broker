from local_inference_broker.settings import Settings


def test_loopback_ipv6_does_not_require_token() -> None:
    Settings(host="::1").validate_network_boundary()


def test_lan_binding_with_token_is_allowed() -> None:
    Settings(host="192.0.2.10", bearer_token="synthetic-test-token").validate_network_boundary()


def test_localhost_does_not_require_token() -> None:
    Settings(host="localhost").validate_network_boundary()
