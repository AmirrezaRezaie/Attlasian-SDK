import httpx
import pytest

from confluence_sdk.client import ConfluenceClient
from confluence_sdk.connection import Connection, ConnectionConfig


def mock_transport(json_body, status_code=200):
    def handler(request):
        return httpx.Response(status_code=status_code, json=json_body)

    return httpx.MockTransport(handler)


def test_get_page_success():
    transport = mock_transport({"id": "123", "type": "page"})
    client = ConfluenceClient(
        base_url="https://example.com/wiki",
        username="user",
        auth_token="token",
        connection=Connection(
            ConnectionConfig(
                base_url="https://example.com/wiki",
                username="user",
                auth_token="token",
            ),
            client=httpx.Client(transport=transport),
        ),
    )

    result = client.get_page("123")
    assert result["id"] == "123"
    assert result["type"] == "page"


def test_get_page_not_found():
    transport = mock_transport({"message": "missing"}, status_code=404)
    client = ConfluenceClient(
        base_url="https://example.com/wiki",
        username="user",
        auth_token="token",
        connection=Connection(
            ConnectionConfig(
                base_url="https://example.com/wiki",
                username="user",
                auth_token="token",
            ),
            client=httpx.Client(transport=transport),
        ),
    )

    with pytest.raises(Exception):
        client.get_page("does-not-exist")

