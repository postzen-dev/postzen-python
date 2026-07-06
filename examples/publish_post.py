"""Publish a post immediately."""

from __future__ import annotations

from postzen import PostZen
from postzen.client.exceptions import PostZenAPIError


def main() -> None:
    client = PostZen()

    try:
        accounts = client.accounts.list_accounts()
        account = accounts.accounts[0]
        result = client.posts.create_post(
            content="Hello from PostZen",
            platforms=[{"platform": account.platform, "accountId": account.field_id}],
            publish_now=True,
        )
        print(result.post.field_id)
    except PostZenAPIError as exc:
        print(f"PostZen API error: {exc}")


if __name__ == "__main__":
    main()
