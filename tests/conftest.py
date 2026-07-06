"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from postzen import PostZen


@pytest.fixture
def api_key() -> str:
    return "postzen_test_key"


@pytest.fixture
def base_url() -> str:
    return "https://api.test.postzen.dev"


@pytest.fixture
def client(api_key: str, base_url: str) -> PostZen:
    return PostZen(api_key=api_key, base_url=base_url)


@pytest.fixture
def profile_payload() -> dict:
    return {
        "_id": "prof_123",
        "userId": "user_123",
        "name": "Main",
        "description": "Primary profile",
        "color": "#ffeda0",
        "isDefault": True,
        "createdAt": "2026-01-01T00:00:00Z",
    }


@pytest.fixture
def account_payload() -> dict:
    return {
        "_id": "acc_123",
        "platform": "instagram",
        "providerAccountId": "provider_123",
        "profileId": {
            "_id": "prof_123",
            "name": "Main",
            "slug": "main",
            "color": "#ffeda0",
        },
        "username": "postzen",
        "displayName": "PostZen",
        "profileUrl": "https://example.com/postzen",
        "avatarUrl": "https://example.com/avatar.png",
        "status": "connected",
        "isActive": True,
        "connectedAt": "2026-01-01T00:00:00Z",
    }


@pytest.fixture
def api_post_payload() -> dict:
    return {
        "_id": "post_123",
        "title": "Launch",
        "content": "Publishing from PostZen",
        "status": "published",
        "scheduledFor": None,
        "timezone": "UTC",
        "platforms": [
            {
                "platform": "instagram",
                "accountId": {
                    "_id": "acc_123",
                    "platform": "instagram",
                    "username": "postzen",
                    "displayName": "PostZen",
                    "isActive": True,
                },
                "status": "published",
                "platformPostUrl": "https://example.com/p/123",
            }
        ],
    }
