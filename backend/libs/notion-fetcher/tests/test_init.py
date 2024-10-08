import pytest
from notion_fetcher import fetch_notion_pages


@pytest.mark.asyncio
async def test_fetch_notion_rs():
    await fetch_notion_pages()
