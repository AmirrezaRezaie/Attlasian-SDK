import httpx
import pytest

from jira_sdk.client import JiraClient
from jira_sdk.connection import JiraConnection, JiraConnectionConfig
from jira_sdk.exceptions import JiraNotFound


def mock_transport(json_body, status_code=200):
    def handler(request):
        return httpx.Response(status_code=status_code, json=json_body)

    return httpx.MockTransport(handler)


def build_client(transport):
    return JiraClient(
        base_url="https://example.com",
        username="user",
        auth_token="token",
        connection=JiraConnection(
            JiraConnectionConfig(
                base_url="https://example.com",
                username="user",
                auth_token="token",
            ),
            client=httpx.Client(transport=transport),
        ),
    )


def test_get_issue_success():
    transport = mock_transport({"key": "ABC-1", "fields": {"summary": "Test"}})
    client = build_client(transport)

    result = client.get_issue("ABC-1")
    assert result["key"] == "ABC-1"
    assert result["fields"]["summary"] == "Test"


def test_get_issue_not_found():
    transport = mock_transport({"errorMessages": ["missing"]}, status_code=404)
    client = build_client(transport)

    with pytest.raises(JiraNotFound):
        client.get_issue("MISSING-1")

