"""Hand-written media resource with a one-step upload helper.

This module is a MANUAL override of the generated ``media`` resource. The
generator (`scripts/generate_resources.py`) detects this file and points
`resources/__init__.py` at it instead of `._generated.media`, so the
``upload`` / ``aupload`` helpers below survive regeneration. The presign
methods (``create_media_presign`` / ``acreate_media_presign``) are inherited
unchanged from the generated base class.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

from ..client.exceptions import PostZenAPIError
from ..models import MediaUploadResult
from ._generated.media import MediaResource as _GeneratedMediaResource

if TYPE_CHECKING:
    from ..models import MediaPresignResponse

# Extension -> presign contentType enum. Mirrors the CLI's media:upload map and
# the presign request schema. Keep the two in sync.
_CONTENT_TYPES: dict[str, str] = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
    "mp4": "video/mp4",
    "mpeg": "video/mpeg",
    "mpg": "video/mpeg",
    "mov": "video/quicktime",
    "avi": "video/x-msvideo",
    "webm": "video/webm",
    "m4v": "video/x-m4v",
    "pdf": "application/pdf",
}


def _extension(name: str) -> str:
    """Return the lowercased extension of ``name`` without the leading dot."""
    return Path(name).suffix.lstrip(".").lower()


def _infer_content_type(ext_source: str) -> str:
    """Map a filename/path extension to a presign contentType, or raise ValueError."""
    ext = _extension(ext_source)
    content_type = _CONTENT_TYPES.get(ext)
    if content_type is None:
        raise ValueError(
            f'Cannot infer content type from extension ".{ext}". '
            "Pass content_type explicitly (e.g. content_type=\"image/png\")."
        )
    return content_type


def _prepare_upload(
    source: str | bytes | bytearray | os.PathLike[str],
    filename: str | None,
    content_type: str | None,
) -> tuple[bytes, str, str, int]:
    """Resolve raw bytes, filename, content type, and size before any network call.

    Returns ``(data, filename, content_type, size)``.
    """
    if isinstance(source, (bytes, bytearray)):
        if not filename:
            raise ValueError(
                "filename is required when uploading raw bytes "
                "(e.g. client.media.upload(data, filename=\"photo.jpg\"))."
            )
        data = bytes(source)
        resolved_filename = filename
        ext_source = filename
    else:
        # Path input. Reading the bytes also validates the file exists and is
        # readable; a missing/unreadable path raises OSError before any request.
        path = Path(os.fspath(source))
        data = path.read_bytes()
        resolved_filename = filename or path.name
        # Infer the content type from the original path extension (parity with
        # the CLI), even when a custom filename is supplied.
        ext_source = path.name

    resolved_content_type = content_type or _infer_content_type(ext_source)
    return data, resolved_filename, resolved_content_type, len(data)


def _build_result(
    presign: MediaPresignResponse, size: int, filename: str
) -> MediaUploadResult:
    return MediaUploadResult(
        public_url=presign.publicUrl,
        key=presign.key,
        type=presign.type,
        size=size,
        filename=filename,
    )


class MediaResource(_GeneratedMediaResource):
    """Create presigned media upload URLs and upload media in one step."""

    def upload(
        self,
        source: str | bytes | bytearray | os.PathLike[str],
        *,
        filename: str | None = None,
        content_type: str | None = None,
        profile_id: str | None = None,
    ) -> MediaUploadResult:
        """Upload a file (path or raw bytes) and return its public URL.

        Presigns an upload slot, PUTs the raw bytes to PostZen-hosted storage,
        and returns a :class:`MediaUploadResult` whose ``public_url`` can be used
        in ``posts.create_post`` ``media_items``.

        ``source`` is a file path (``str`` / ``os.PathLike``) or raw ``bytes``.
        When bytes are passed, ``filename`` is required. ``content_type`` is
        inferred from the extension when omitted.
        """
        data, resolved_filename, resolved_content_type, size = _prepare_upload(
            source, filename, content_type
        )

        presign = self.create_media_presign(
            filename=resolved_filename,
            content_type=resolved_content_type,
            size=size,
            profile_id=profile_id,
        )

        with httpx.Client(timeout=self._client.timeout) as http:
            response = http.put(
                presign.uploadUrl,
                content=data,
                headers={"content-type": resolved_content_type},
            )
        if not response.is_success:
            raise PostZenAPIError(
                "upload to presigned URL failed",
                status_code=response.status_code,
            )

        return _build_result(presign, size, resolved_filename)

    async def aupload(
        self,
        source: str | bytes | bytearray | os.PathLike[str],
        *,
        filename: str | None = None,
        content_type: str | None = None,
        profile_id: str | None = None,
    ) -> MediaUploadResult:
        """Upload a file (path or raw bytes) and return its public URL (async)."""
        data, resolved_filename, resolved_content_type, size = _prepare_upload(
            source, filename, content_type
        )

        presign = await self.acreate_media_presign(
            filename=resolved_filename,
            content_type=resolved_content_type,
            size=size,
            profile_id=profile_id,
        )

        async with httpx.AsyncClient(timeout=self._client.timeout) as http:
            response = await http.put(
                presign.uploadUrl,
                content=data,
                headers={"content-type": resolved_content_type},
            )
        if not response.is_success:
            raise PostZenAPIError(
                "upload to presigned URL failed",
                status_code=response.status_code,
            )

        return _build_result(presign, size, resolved_filename)
