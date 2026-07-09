# PostZen Python SDK

Official Python SDK for the [PostZen](https://postzen.dev) social publishing API — manage profiles, connect social accounts, upload media, and schedule or publish posts against `https://api.postzen.dev`. Fully typed with pydantic, sync and async.

[![PyPI version](https://img.shields.io/pypi/v/postzen-sdk)](https://pypi.org/project/postzen-sdk/) [![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://pypi.org/project/postzen-sdk/) [![python versions](https://img.shields.io/pypi/pyversions/postzen-sdk)](https://pypi.org/project/postzen-sdk/)

This package is auto-generated: when the [PostZen OpenAPI spec](https://docs.postzen.dev/api-reference) changes, CI regenerates the resources, models, and the reference below from `openapi.json` and publishes a new release, so the SDK always matches the current API. The same pipeline keeps the [Node.js SDK](https://github.com/postzen-dev/postzen-node), the [CLI](https://github.com/postzen-dev/postzen-cli), and the [MCP server](https://docs.postzen.dev/mcp) in sync.

## Installation

```bash
pip install postzen-sdk
```

The import name is `postzen`. Requires Python 3.10+.

## Quick Start

Set `POSTZEN_API_KEY` and create a post:

```python
from postzen import PostZen

client = PostZen()

post = client.posts.create_post(
    content="Hello from PostZen",
    platforms=[{"platform": "instagram", "accountId": "acc_123"}],
    publish_now=True,
)

print(post.post.field_id)
```

Wire fields named `_id` are exposed as `field_id` on pydantic models, so a profile id is available as `profile.field_id`.

## Authentication

The client authenticates with a bearer API key, resolved in this order:

1. The `api_key` argument passed to `PostZen(...)`.
2. The `POSTZEN_API_KEY` environment variable.

If neither is set, `PostZen()` raises `ValueError`.

```python
from postzen import PostZen

# Explicit key
client = PostZen(api_key="pzn_live_...")

# Or rely on POSTZEN_API_KEY in the environment
client = PostZen()
```

## Configuration

```python
from postzen import PostZen

client = PostZen(
    api_key="pzn_live_...",
    base_url="https://api.postzen.dev",
    timeout=30.0,
    max_retries=3,
)
```

| Option | Description | Default |
|--------|-------------|---------|
| `api_key` | PostZen API key. If omitted, `POSTZEN_API_KEY` is used. | `None` |
| `base_url` | API base URL. Useful for tests and staging. | `https://api.postzen.dev` |
| `timeout` | Request timeout in seconds. | `30.0` |
| `max_retries` | Retries for connection errors and idempotent-method timeouts. See [Retry behavior](#retry-behavior). | `3` |

## Examples

### Schedule a Post

```python
from postzen import PostZen

client = PostZen()

client.posts.create_post(
    content="Scheduled from PostZen",
    platforms=[{"platform": "linkedin", "accountId": "acc_123"}],
    scheduled_for="2026-08-01T15:00:00Z",
    timezone="America/New_York",
)
```

### Platform-Specific Content

```python
from postzen import PostZen

client = PostZen()

client.posts.create_post(
    content="Shared copy",
    platforms=[
        {
            "platform": "instagram",
            "accountId": "acc_ig",
            "customContent": "Instagram copy",
            "settings": {"postType": "reel", "firstComment": "#postzen"},
        },
        {
            "platform": "youtube",
            "accountId": "acc_yt",
            "settings": {"title": "Launch update", "privacyStatus": "public"},
        },
    ],
    publish_now=True,
)
```

### Upload Media

```python
from pathlib import Path

import httpx

from postzen import PostZen

client = PostZen()
path = Path("image.png")

presign = client.media.create_media_presign(
    filename=path.name,
    content_type="image/png",
    size=path.stat().st_size,
)

httpx.put(
    presign.uploadUrl,
    content=path.read_bytes(),
    headers={"Content-Type": "image/png"},
).raise_for_status()

client.posts.create_post(
    content="Media post",
    media_items=[{"url": presign.publicUrl}],
    publish_now=True,
)
```

### List Connected Accounts

```python
from postzen import PostZen

client = PostZen()

accounts = client.accounts.list_accounts(platform="instagram")
for account in accounts.accounts:
    print(account.field_id, account.username)
```

### Paginate Accounts

`list_accounts` accepts `page` and `limit` (max 100) and returns a `pagination` object with `page`, `limit`, `total`, and `totalPages`.

```python
from postzen import PostZen

client = PostZen()

page = 1
while True:
    result = client.accounts.list_accounts(page=page, limit=50)
    for account in result.accounts:
        print(account.field_id, account.username)

    pagination = result.pagination
    if not pagination or page >= pagination.totalPages:
        break
    page += 1
```

### Async Support

```python
import asyncio

from postzen import PostZen


async def main():
    async with PostZen() as client:
        profiles = await client.profiles.alist_profiles()
        print(profiles.profiles)


asyncio.run(main())
```

## Error Handling

```python
from postzen import PostZen
from postzen.client.exceptions import PostZenAPIError, PostZenRateLimitError

client = PostZen()

try:
    client.posts.create_post(content="Hello", publish_now=True)
except PostZenRateLimitError as exc:
    print(exc.limit, exc.remaining, exc.reset_time)
except PostZenAPIError as exc:
    print(exc.status_code, exc.details)
```

Exception hierarchy:

| Exception | Meaning |
|-----------|---------|
| `PostZenError` | Base SDK exception |
| `PostZenAPIError` | Base API response exception |
| `PostZenAuthenticationError` | HTTP 401 |
| `PostZenPaymentRequiredError` | HTTP 402 |
| `PostZenForbiddenError` | HTTP 403 |
| `PostZenNotFoundError` | HTTP 404 |
| `PostZenRateLimitError` | HTTP 429 with `limit`, `remaining`, and `reset_time` |
| `PostZenConnectionError` | Connection failure after retries |
| `PostZenTimeoutError` | Timeout after retries |
| `PostZenValidationError` | Client-side validation error |

The client updates `client.rate_limit_info` from `X-RateLimit-*` headers on every response.

### Retry behavior

Connection errors (the connection never opened) are always retried with exponential backoff, up to `max_retries`. Timeouts are retried only on idempotent methods (`GET`, `PUT`, `DELETE`); a read/write timeout on a `POST` — such as `create_post` — is *not* retried, because the request may have already reached the server and an automatic retry could silently create a duplicate. Instead, `PostZenTimeoutError` is raised immediately. To retry a `POST` safely, pass a stable `x_request_id` to `create_post` so the server treats the replay as idempotent:

```python
client.posts.create_post(
    content="Hello from PostZen",
    platforms=[{"platform": "instagram", "accountId": "acc_123"}],
    publish_now=True,
    x_request_id="a1b2c3d4-launch-2026-08-01",
)
```

## SDK Reference

### Profiles
| Method | Description |
|--------|-------------|
| `profiles.list_profiles()` | List profiles |
| `profiles.create_profile()` | Create a profile |
| `profiles.get_profile()` | Get a profile |
| `profiles.update_profile()` | Update a profile |
| `profiles.delete_profile()` | Delete a profile |

### Accounts
| Method | Description |
|--------|-------------|
| `accounts.list_accounts()` | List accounts |
| `accounts.disconnect_account()` | Disconnect an account |

### Connect (OAuth)
| Method | Description |
|--------|-------------|
| `connect.create_connect_url()` | Create an OAuth connect URL |
| `connect.complete_connect()` | Complete an OAuth connection |

### Media
| Method | Description |
|--------|-------------|
| `media.create_media_presign()` | Create a presigned media upload URL |

### Posts
| Method | Description |
|--------|-------------|
| `posts.create_post()` | Create a post |

## Requirements

- Python 3.10 or later
- A PostZen API key ([create one](https://app.postzen.dev/api-keys))

Runtime dependencies:

- `httpx>=0.27.0`
- `pydantic>=2.0.0`

## Development

```bash
pip install -e ".[dev]"                      # install the SDK with dev dependencies
python scripts/generate_readme_reference.py  # regenerate the SDK Reference section above
pytest                                        # run the test suite
```

`openapi.json` and everything under `src/postzen/models/_generated/` and `src/postzen/resources/_generated/` are synced from the PostZen monorepo and regenerated by CI — don't edit them by hand.

## PostZen developer tools

- [Documentation](https://docs.postzen.dev)
- [API reference](https://docs.postzen.dev/api-reference)
- [Node.js SDK](https://github.com/postzen-dev/postzen-node) — `@postzen/node`
- [CLI](https://github.com/postzen-dev/postzen-cli) — `@postzen/cli`
- [MCP server](https://docs.postzen.dev/mcp)
- [Dashboard & API keys](https://app.postzen.dev/api-keys)

## License

MIT
