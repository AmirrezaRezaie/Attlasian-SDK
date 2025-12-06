# Confluence & Jira SDK (starter)

A starter scaffold for lightweight Confluence and Jira REST clients in Python. It includes a `src/`-style package layout, packaging config via `pyproject.toml`, minimal dependencies, and simple modules for connection and API calls.

## Features
- `src/` package layout.
- Connection handling and auth headers in `connection.py`.
- Thin clients in `client.py` with a few sample methods (read/create page for Confluence, issue operations for Jira).
- Dedicated exceptions per SDK.
- Basic tests with `pytest`.

## Requirements
- Python 3.10+
- pip >= 23

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Run tests
```bash
pytest
```

## Quick usage
```python
from confluence_sdk.client import ConfluenceClient
from jira_sdk.client import JiraClient

confluence = ConfluenceClient(
    base_url="https://your-domain.atlassian.net/wiki",
    auth_token="your-api-token",
    username="your-email@example.com",
)

page = confluence.get_page(page_id="12345")
print(page)

jira = JiraClient(
    base_url="https://your-domain.atlassian.net",
    auth_token="your-api-token",
    username="your-email@example.com",
)

issue = jira.get_issue(issue_key="ABC-1")
print(issue)
```

## TODO
- Add more Confluence API coverage.
- Add more Jira API coverage (transition, comment, attachment).
- Add retry and logging.
- Handle pagination helpers.

