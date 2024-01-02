import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()
    print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))  # For debugging


@pytest.fixture(scope="session", autouse=True)
def verify_env_variables():
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_KEY",
        "OPENAI_API_KEY",
        "JWT_SECRET_KEY",
        "CELERY_BROKER_URL",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        missing_vars_str = ", ".join(missing_vars)
        pytest.fail(f"Required environment variables are missing: {missing_vars_str}")


@pytest.fixture(scope="module")
def client():
    from main import app

    return TestClient(app)


@pytest.fixture(scope="module")
def api_key():
    API_KEY = os.getenv("CI_TEST_API_KEY")
    if not API_KEY:
        raise ValueError(
            "CI_TEST_API_KEY environment variable not set. Cannot run tests."
        )
    return API_KEY
