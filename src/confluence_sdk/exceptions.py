class ConfluenceError(Exception):
    """Base exception for Confluence SDK."""


class ConfluenceAuthError(ConfluenceError):
    """Raised on authentication or permission errors."""


class ConfluenceNotFound(ConfluenceError):
    """Raised when a requested resource is missing."""

