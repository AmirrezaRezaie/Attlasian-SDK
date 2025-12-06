from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, HttpUrl, validator


class ConnectionConfig(BaseModel):
    base_url: HttpUrl
    username: str
    auth_token: str
    timeout_seconds: float = 10.0
    verify_ssl: bool = True

    @validator("base_url", pre=True)
    def ensure_trailing_slash(cls, value: str) -> str:  # pylint: disable=no-self-argument
        # Confluence base urls often end with /wiki; normalizing avoids double-slashes later.
        if not value.endswith("/"):
            return f"{value}/"
        return value


class Connection:
    """
    Thin wrapper around httpx.Client to keep headers and URL construction in one place.
    """

    def __init__(self, config: ConnectionConfig, client: Optional[httpx.Client] = None) -> None:
        self.config = config
        self._client = client or httpx.Client(
            base_url=str(config.base_url),
            timeout=config.timeout_seconds,
            verify=config.verify_ssl,
        )

    def build_headers(self) -> Dict[str, str]:
        token = httpx.BasicAuth(self.config.username, self.config.auth_token)
        return {
            "Authorization": token.auth_header.decode("utf-8"),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        url = urljoin(str(self.config.base_url), path)
        return self._client.request(
            method=method,
            url=url,
            params=params,
            json=json,
            headers=self.build_headers(),
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "Connection":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

