import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import httpx
import pytest
from notion_client.client import Client

from quivr_api.modules.sync.entity.notion_page import NotionPage
from quivr_api.modules.sync.service.sync_notion import (
    fetch_limit_notion_pages,
    fetch_notion_pages,
)


@pytest.fixture(scope="function")
def page_response() -> dict[str, Any]:
    json_path = (
        Path(os.getenv("PYTEST_CURRENT_TEST").split(":")[0])
        .parent.absolute()
        .joinpath("page.json")
    )
    with open(json_path, "r") as f:
        page = json.load(f)
    return page


@pytest.fixture(scope="function")
def fetch_response():
    return [
        {
            "object": "page",
            "id": "27b26c5a-e86f-470a-a5fc-27a3fc308850",
            "created_time": "2024-05-02T09:03:00.000Z",
            "last_edited_time": "2024-08-19T10:01:00.000Z",
            "created_by": {
                "object": "user",
                "id": "e2f8bfda-3b98-466e-a2c1-39e5f0f64881",
            },
            "last_edited_by": {
                "object": "user",
                "id": "f87bcc4b-68ee-4d44-b518-3d2d19ffedc2",
            },
            "cover": None,
            "icon": {"type": "emoji", "emoji": "🌇"},
            "parent": {"type": "workspace", "workspace": True},
            "archived": False,
            "in_trash": False,
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "Investors", "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": "Investors",
                            "href": None,
                        }
                    ],
                }
            },
            "url": "https://www.notion.so/Investors-27b26c5ae86f470aa5fc27a3fc308850",
            "public_url": None,
        },
        {
            "object": "page",
            "id": "ff799030-eae6-4c81-8631-ee2653f27af8",
            "created_time": "2024-04-04T23:24:00.000Z",
            "last_edited_time": "2024-08-19T10:01:00.000Z",
            "created_by": {
                "object": "user",
                "id": "c8de6079-cc5a-4b46-8763-04f92b33fc18",
            },
            "last_edited_by": {
                "object": "user",
                "id": "f87bcc4b-68ee-4d44-b518-3d2d19ffedc2",
            },
            "cover": None,
            "icon": {"type": "emoji", "emoji": "🎓"},
            "parent": {"type": "workspace", "workspace": True},
            "archived": False,
            "in_trash": False,
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "Academy", "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": "Academy",
                            "href": None,
                        }
                    ],
                }
            },
            "url": "https://www.notion.so/Academy-ff799030eae64c818631ee2653f27af8",
            "public_url": None,
        },
    ]


def test_deserialize_notion_page(fetch_response):
    page = NotionPage.model_validate(fetch_response[0])  # type: ignore
    assert page


def test_fetch_notion_pages(fetch_response):
    def handler(request):
        return httpx.Response(
            200,
            json={"results": fetch_response, "has_more": False, "next_cursor": None},
        )

    _client = httpx.Client(transport=httpx.MockTransport(handler))
    notion_client = Client(client=_client)

    result = fetch_notion_pages(notion_client)
    assert len(result.results) == 2
    assert not result.has_more
    assert result.next_cursor is None


# TODO(@aminediro): test more cases: noresponse, error, no  has_more ..
def test_fetch_limit_notion_pages(fetch_response):
    def handler(request):
        return httpx.Response(
            200,
            json={"results": fetch_response, "has_more": False, "next_cursor": None},
        )

    _client = httpx.Client(transport=httpx.MockTransport(handler))
    notion_client = Client(client=_client)

    result = fetch_limit_notion_pages(
        notion_client, datetime.now() - timedelta(hours=6)
    )

    assert len(result) == len(fetch_response)


def test_fetch_limit_notion_pages_now(fetch_response):
    def handler(request):
        return httpx.Response(
            200,
            json={"results": fetch_response, "has_more": False, "next_cursor": None},
        )

    _client = httpx.Client(transport=httpx.MockTransport(handler))
    notion_client = Client(client=_client)

    result = fetch_limit_notion_pages(notion_client, datetime.now())

    assert len(result) == 0
