"""Hand-written models for the one-step media upload helper.

This module is NOT generated. `scripts/generate_models.py` only writes files
under `models/_generated/`, so the model defined here survives regeneration.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MediaUploadResult(BaseModel):
    """Result of a one-step ``client.media.upload(...)`` call.

    Combines the presign response (``public_url``, ``key``, ``type``) with the
    locally known ``size`` and ``filename`` of the uploaded bytes.
    """

    model_config = ConfigDict(populate_by_name=True)

    public_url: str
    key: str
    type: str
    size: int
    filename: str
