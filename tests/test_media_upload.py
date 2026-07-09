"""Tests for the one-step media upload helper (client.media.upload / aupload)."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import httpx
import pytest
import respx

from postzen.client.exceptions import PostZenAPIError, PostZenPaymentRequiredError

if TYPE_CHECKING:
    from pathlib import Path

UPLOAD_URL = "https://uploads.example.com/object"
PUBLIC_URL = "https://cdn.example.com/object"

PRESIGN_RESPONSE = {
    "uploadUrl": UPLOAD_URL,
    "publicUrl": PUBLIC_URL,
    "key": "object-key",
    "type": "image",
}


def _mock_presign(base_url: str, status: int = 200, json_body: dict | None = None):
    return respx.post(f"{base_url}/v1/media/presign").mock(
        return_value=httpx.Response(status, json=json_body or PRESIGN_RESPONSE)
    )


def _mock_upload(status: int = 200):
    return respx.put(UPLOAD_URL).mock(return_value=httpx.Response(status))


@respx.mock
def test_upload_from_file(client, base_url: str, tmp_path: Path) -> None:
    presign_route = _mock_presign(base_url)
    upload_route = _mock_upload()

    data = b"\x89PNG\r\n\x1a\n binary bytes"
    file_path = tmp_path / "photo.png"
    file_path.write_bytes(data)

    result = client.media.upload(str(file_path), profile_id="prof_123")

    # Presign request body: inferred contentType + correct size + filename + profileId.
    presign_body = json.loads(presign_route.calls[0].request.content)
    assert presign_body["filename"] == "photo.png"
    assert presign_body["contentType"] == "image/png"
    assert presign_body["size"] == len(data)
    assert presign_body["profileId"] == "prof_123"

    # PUT delivers the exact bytes with the right content-type and no auth header.
    put_request = upload_route.calls[0].request
    assert put_request.content == data
    assert put_request.headers["content-type"] == "image/png"
    assert "authorization" not in put_request.headers
    assert str(put_request.url) == UPLOAD_URL

    # Result fields.
    assert result.public_url == PUBLIC_URL
    assert result.key == "object-key"
    assert result.type == "image"
    assert result.size == len(data)
    assert result.filename == "photo.png"


@respx.mock
def test_upload_from_bytes_with_filename(client, base_url: str) -> None:
    presign_route = _mock_presign(base_url)
    upload_route = _mock_upload()

    data = b"raw jpeg bytes"
    result = client.media.upload(data, filename="picture.jpg")

    presign_body = json.loads(presign_route.calls[0].request.content)
    assert presign_body["filename"] == "picture.jpg"
    assert presign_body["contentType"] == "image/jpeg"
    assert presign_body["size"] == len(data)
    assert "profileId" not in presign_body

    assert upload_route.calls[0].request.content == data
    assert upload_route.calls[0].request.headers["content-type"] == "image/jpeg"
    assert result.filename == "picture.jpg"
    assert result.size == len(data)


@respx.mock
def test_upload_explicit_content_type_overrides_inference(client, base_url: str) -> None:
    presign_route = _mock_presign(base_url)
    _mock_upload()

    client.media.upload(b"data", filename="clip.bin", content_type="video/mp4")

    presign_body = json.loads(presign_route.calls[0].request.content)
    assert presign_body["contentType"] == "video/mp4"


def test_upload_bytes_without_filename_raises(client) -> None:
    with pytest.raises(ValueError, match="filename is required"):
        client.media.upload(b"data")


def test_upload_unknown_extension_raises(client, tmp_path: Path) -> None:
    file_path = tmp_path / "archive.xyz"
    file_path.write_bytes(b"data")

    with pytest.raises(ValueError, match="content_type") as exc:
        client.media.upload(str(file_path))
    assert ".xyz" in str(exc.value)


def test_upload_missing_file_raises_before_network(client) -> None:
    # No respx.mock active: if a request were made it would error differently.
    with pytest.raises(OSError):
        client.media.upload("/nonexistent/path/does-not-exist.png")


@respx.mock
def test_upload_presign_error_propagates(client, base_url: str, tmp_path: Path) -> None:
    _mock_presign(base_url, status=402, json_body={"error": "Payment required"})
    upload_route = _mock_upload()

    file_path = tmp_path / "photo.png"
    file_path.write_bytes(b"data")

    with pytest.raises(PostZenPaymentRequiredError):
        client.media.upload(str(file_path))
    # Presign failed -> the PUT must never happen.
    assert not upload_route.called


@respx.mock
def test_upload_put_failure_raises_with_status(client, base_url: str, tmp_path: Path) -> None:
    _mock_presign(base_url)
    _mock_upload(status=403)

    file_path = tmp_path / "photo.png"
    file_path.write_bytes(b"data")

    with pytest.raises(PostZenAPIError) as exc:
        client.media.upload(str(file_path))
    assert exc.value.status_code == 403
    assert "upload to presigned URL failed" in str(exc.value)


@respx.mock
async def test_aupload_from_file(client, base_url: str, tmp_path: Path) -> None:
    presign_route = _mock_presign(base_url)
    upload_route = _mock_upload()

    data = b"async png bytes"
    file_path = tmp_path / "async.png"
    file_path.write_bytes(data)

    result = await client.media.aupload(str(file_path))

    presign_body = json.loads(presign_route.calls[0].request.content)
    assert presign_body["contentType"] == "image/png"
    assert presign_body["size"] == len(data)

    put_request = upload_route.calls[0].request
    assert put_request.content == data
    assert put_request.headers["content-type"] == "image/png"
    assert "authorization" not in put_request.headers
    assert result.public_url == PUBLIC_URL
    assert result.size == len(data)


@respx.mock
async def test_aupload_bytes_without_filename_raises(client) -> None:
    with pytest.raises(ValueError, match="filename is required"):
        await client.media.aupload(b"data")


@respx.mock
async def test_aupload_put_failure_raises_with_status(client, base_url: str) -> None:
    _mock_presign(base_url)
    _mock_upload(status=500)

    with pytest.raises(PostZenAPIError) as exc:
        await client.media.aupload(b"data", filename="x.png")
    assert exc.value.status_code == 500
    assert "upload to presigned URL failed" in str(exc.value)
