# PostZen Python SDK

Official Python SDK for the PostZen Public API. Use it to manage profiles, connected social accounts, media uploads, and post publishing.

## Installation

```bash
pip install postzen-sdk
```

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

## Configuration

```python
from postzen import PostZen

client = PostZen(
    api_key="pz_...",
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

Python 3.10+

Runtime dependencies:

- `httpx>=0.27.0`
- `pydantic>=2.0.0`

## Links

- Documentation: https://docs.postzen.dev/
- App: https://app.postzen.dev/
- Website: https://postzen.dev
- GitHub: https://github.com/postzen-dev/postzen-python

## License

MIT
