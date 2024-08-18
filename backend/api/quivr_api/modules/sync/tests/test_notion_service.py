import json
import os
from pathlib import Path
from pprint import pprint
from typing import Any

import pytest

from quivr_api.modules.sync.entity.notion_page import NotionPage


@pytest.fixture
def page_response() -> dict[str, Any]:
    json_path = (
        Path(os.getenv("PYTEST_CURRENT_TEST").split(":")[0])
        .parent.absolute()
        .joinpath("page.json")
    )

    with open(json_path, "r") as f:
        page = json.load(f)
    return page


def test_deserialize_notion_page(page_response):
    page = NotionPage.model_validate(page_response)

    pprint(page.model_dump())
