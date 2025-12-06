from typing import Any, Dict, Optional

from .connection import Connection, ConnectionConfig
from .exceptions import ConfluenceAuthError, ConfluenceError, ConfluenceNotFound


class ConfluenceClient:
    """
    Minimal Confluence REST client. Extend or wrap methods below to grow coverage.
    """

    def __init__(
        self,
        base_url: str,
        auth_token: str,
        username: str,
        connection: Optional[Connection] = None,
        timeout_seconds: float = 10.0,
    ) -> None:
        self.connection = connection or Connection(
            ConnectionConfig(
                base_url=base_url,
                username=username,
                auth_token=auth_token,
                timeout_seconds=timeout_seconds,
            )
        )

    def get_page(self, page_id: str, expand: Optional[str] = None) -> Dict[str, Any]:
        params = {"expand": expand} if expand else None
        response = self.connection.request(
            method="GET",
            path=f"/rest/api/content/{page_id}",
            params=params,
        )
        return self._parse_response(response)

    def create_page(
        self,
        space_key: str,
        title: str,
        body_storage: str,
        parent_page_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        ancestors = [{"id": parent_page_id}] if parent_page_id else []
        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": body_storage,
                    "representation": "storage",
                }
            },
        }
        if ancestors:
            payload["ancestors"] = ancestors

        response = self.connection.request(
            method="POST",
            path="/rest/api/content",
            json=payload,
        )
        return self._parse_response(response, expected_status=201)

    def search(self, cql: str, limit: int = 25) -> Dict[str, Any]:
        params = {"cql": cql, "limit": limit}
        response = self.connection.request(
            method="GET",
            path="/rest/api/content/search",
            params=params,
        )
        return self._parse_response(response)

    def _parse_response(self, response, expected_status: int = 200) -> Dict[str, Any]:
        if response.status_code in (401, 403):
            raise ConfluenceAuthError(f"Authentication failed: {response.text}")
        if response.status_code == 404:
            raise ConfluenceNotFound("Resource not found")
        if response.status_code not in (expected_status, 200):
            raise ConfluenceError(f"Unexpected status {response.status_code}: {response.text}")
        try:
            return response.json()
        except ValueError as exc:
            raise ConfluenceError("Response payload is not JSON") from exc

