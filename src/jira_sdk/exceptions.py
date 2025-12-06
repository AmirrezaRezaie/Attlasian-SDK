class JiraError(Exception):
    """Base exception for Jira SDK."""


class JiraAuthError(JiraError):
    """Raised on authentication or permission errors."""


class JiraNotFound(JiraError):
    """Raised when a requested resource is missing."""

