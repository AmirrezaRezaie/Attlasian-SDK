"""
Public API for the Confluence SDK starter.
"""

from .client import ConfluenceClient
from .connection import Connection, ConnectionConfig
from .exceptions import ConfluenceError, ConfluenceAuthError, ConfluenceNotFound

__all__ = [
    "ConfluenceClient",
    "Connection",
    "ConnectionConfig",
    "ConfluenceError",
    "ConfluenceAuthError",
    "ConfluenceNotFound",
]

