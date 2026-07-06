"""Async SDK usage."""

from __future__ import annotations

import asyncio

from postzen import PostZen


async def main() -> None:
    async with PostZen() as client:
        accounts = await client.accounts.alist_accounts()
        account = accounts.accounts[0]
        post = await client.posts.acreate_post(
            content="Async publishing with PostZen",
            platforms=[{"platform": account.platform, "accountId": account.field_id}],
            publish_now=True,
        )
        print(post.post.field_id)


if __name__ == "__main__":
    asyncio.run(main())
