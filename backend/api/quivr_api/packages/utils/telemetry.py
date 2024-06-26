import hashlib
import json
import os
import threading

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
    seed = os.getenv("OPENAI_API_KEY")

    # Use SHA-256 hash to generate a unique key from the seed
    unique_key = hashlib.sha256(seed.encode()).hexdigest()

    return unique_key


def send_telemetry(event_name: str, event_data: dict, request: Request = None):
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

    # Send the telemetry data
    with httpx.Client() as client:
        _ = client.post(TELEMETRY_URL, headers=HEADERS, data=payload)


def maybe_send_telemetry(event_name: str, event_data: dict, request: Request = None):
    enable_telemetry = os.getenv("TELEMETRY_ENABLED", "false")

    if enable_telemetry.lower() != "true":
        return

    threading.Thread(
        target=send_telemetry, args=(event_name, event_data, request)
    ).start()
