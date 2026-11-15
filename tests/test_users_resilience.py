"""Deterministic transport-failure tests; no external HTTP requests are made."""
from unittest.mock import Mock

import pytest
import requests

from api_client import get_user


@pytest.mark.parametrize("failure", [requests.ConnectTimeout, requests.ReadTimeout])
def test_timeout_is_propagated_and_timeout_is_configured(monkeypatch, failure):
    def fake_get(url, timeout):
        assert url == "https://example.test/users/1"
        assert timeout == 3
        raise failure("simulated timeout")

    monkeypatch.setattr("api_client.requests.get", fake_get)
    with pytest.raises(failure):
        get_user("https://example.test", 1, timeout=3)


def test_connection_error_is_propagated(monkeypatch):
    fake_get = Mock(side_effect=requests.ConnectionError("simulated disconnect"))
    monkeypatch.setattr("api_client.requests.get", fake_get)

    with pytest.raises(requests.ConnectionError):
        get_user("https://example.test", 2)

    fake_get.assert_called_once_with("https://example.test/users/2", timeout=10)


def test_new_request_can_succeed_after_previous_connection_failure(monkeypatch):
    response = Mock(status_code=200)
    fake_get = Mock(side_effect=[requests.ConnectionError("offline"), response])
    monkeypatch.setattr("api_client.requests.get", fake_get)

    with pytest.raises(requests.ConnectionError):
        get_user("https://example.test", 1)

    assert get_user("https://example.test", 1) is response
    assert fake_get.call_count == 2
