import os
from uuid import uuid4

from storage3._sync.client import SyncBucketProxy
from supabase import Client

from quivr_worker.process.process_file import build_local_file


def test_build_local_file(monkeypatch):
    def random_bytes(*args, **kwargs):
        return os.urandom(1024)

    client = Client(
        supabase_url="http://localhost:1111",
        # TODO: pytest load from dotenv
        supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU",
    )
    monkeypatch.setattr(SyncBucketProxy, "download", random_bytes)
    brain_id = uuid4()
    file_name = f"{brain_id}/test_file.txt"

    with build_local_file(client, file_name) as file:
        assert len(file.bytes_content) == 1024
        assert file.file_name == "test_file.txt"
