from typing import Any, Dict, Optional

from .connection import JiraConnection, JiraConnectionConfig
from .exceptions import JiraAuthError, JiraError, JiraNotFound


class JiraClient:
    """
    Minimal Jira Cloud REST client. Extend or wrap methods below to grow coverage.
    """

    def __init__(
        self,
        base_url: str,
        auth_token: str,
        username: str,
        connection: Optional[JiraConnection] = None,
        timeout_seconds: float = 10.0,
    ) -> None:
        self.connection = connection or JiraConnection(
            JiraConnectionConfig(
                base_url=base_url,
                username=username,
                auth_token=auth_token,
                timeout_seconds=timeout_seconds,
            )
        )

    def get_issue(self, issue_key: str, fields: Optional[str] = None) -> Dict[str, Any]:
        params = {"fields": fields} if fields else None
        response = self.connection.request(
            method="GET",
            path=f"/rest/api/3/issue/{issue_key}",
            params=params,
        )
        return self._parse_response(response)

    def search(self, jql: str, limit: int = 50, start_at: int = 0) -> Dict[str, Any]:
        payload = {"jql": jql, "maxResults": limit, "startAt": start_at}
        response = self.connection.request(
            method="POST",
            path="/rest/api/3/search",
            json=payload,
        )
        return self._parse_response(response)

    def create_issue(
        self,
        project_key: str,
        summary: str,
        issue_type: str = "Task",
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": issue_type},
            }
        }
        if description:
            payload["fields"]["description"] = description

        response = self.connection.request(
            method="POST",
            path="/rest/api/3/issue",
            json=payload,
        )
        return self._parse_response(response, expected_status=201)

    def _parse_response(self, response, expected_status: int = 200) -> Dict[str, Any]:
        if response.status_code in (401, 403):
            raise JiraAuthError(f"Authentication failed: {response.text}")
        if response.status_code == 404:
            raise JiraNotFound("Resource not found")
        if response.status_code not in (expected_status, 200):
            raise JiraError(f"Unexpected status {response.status_code}: {response.text}")
        try:
            return response.json()
        except ValueError as exc:
            raise JiraError("Response payload is not JSON") from exc

