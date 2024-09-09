import hashlib
import json
import os

import httpx
from fastapi import Request

from quivr_api.logger import get_logger

logger = get_logger(__name__)

# Assume these are your Supabase Function endpoint and any necessary headers
TELEMETRY_URL = "https://ovbvcnwemowuuuaebizd.supabase.co/functions/v1/telemetry"
HEADERS = {
    "Content-Type": "application/json",
}


def generate_machine_key():
    # Get the OpenAI API key from the environment variables
    seed = os.getenv("OPENAI_API_KEY") or ""

    # Use SHA-256 hash to generate a unique key from the seed
    unique_key = hashlib.sha256(seed.encode()).hexdigest()

    return unique_key


def send_telemetry(event_name: str, event_data: dict, request: Request | None = None):
    # Generate a unique machine key
    machine_key = generate_machine_key()
    domain = None
    if request:
        domain = request.url.hostname
        logger.info(f"Domain: {domain}")
        event_data = {**event_data, "domain": domain}
    # Prepare the payload
    payload = json.dumps(
        {
            "anonymous_identifier": machine_key,
            "event_name": event_name,
            "event_data": event_data,
        }
    )

    # TODO: client should only live once
    # Send the telemetry data
    with httpx.Client() as client:
        _ = client.post(TELEMETRY_URL, headers=HEADERS, data=payload)


def maybe_send_telemetry(
    event_name: str,
    event_data: dict,
    request: Request | None = None,
):
    enable_telemetry = os.getenv("TELEMETRY_ENABLED", "false")
    if enable_telemetry.lower() == "false":
        return

    send_telemetry(event_name, event_data, request)
