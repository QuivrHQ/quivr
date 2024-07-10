import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def openai_api_key():
    os.environ["OPENAI_API_KEY"] = "abcd"
