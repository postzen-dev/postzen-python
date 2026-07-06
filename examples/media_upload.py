"""Upload media through a presigned URL, then create a post."""

from __future__ import annotations

from pathlib import Path

import httpx

from postzen import PostZen
from postzen.client.exceptions import PostZenAPIError


def main() -> None:
    client = PostZen()
    path = Path("image.png")
    content_type = "image/png"

    try:
        presign = client.media.create_media_presign(
            filename=path.name,
            content_type=content_type,
            size=path.stat().st_size,
        )
        httpx.put(
            presign.uploadUrl,
            content=path.read_bytes(),
            headers={"Content-Type": content_type},
        ).raise_for_status()
        result = client.posts.create_post(
            content="Uploaded with PostZen",
            media_items=[{"url": presign.publicUrl, "title": "PostZen media"}],
            publish_now=True,
        )
        print(result.post.field_id)
    except (OSError, httpx.HTTPError, PostZenAPIError) as exc:
        print(f"Upload failed: {exc}")


if __name__ == "__main__":
    main()
