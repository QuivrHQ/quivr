import os
import socket

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(".env_test", verbose=True, override=True)

    # Testing socket connection
    host, port = "localhost", 54321
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print(f"Connection to {host} on port {port} succeeded.")
        except socket.error as e:
            print(f"Connection to {host} on port {port} failed: {e}")

    print("Loaded SUPABASE_URL:", os.getenv("SUPABASE_URL"))


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


@pytest.fixture(scope="session")
def client():
    from main import app

    print("CLIENT_SUPABASE_URL:", os.getenv("SUPABASE_URL"))  # For debugging

    return TestClient(app)


@pytest.fixture(scope="session")
def api_key():
    API_KEY = os.getenv("CI_TEST_API_KEY")
    if not API_KEY:
        raise ValueError(
            "CI_TEST_API_KEY environment variable not set. Cannot run tests."
        )
    return API_KEY
