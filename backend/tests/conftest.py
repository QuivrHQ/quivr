import os

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def api_key():
    API_KEY = os.getenv("CI_TEST_API_KEY")
    if not API_KEY:
        raise ValueError(
            "CI_TEST_API_KEY environment variable not set. Cannot run tests."
        )
    return API_KEY
