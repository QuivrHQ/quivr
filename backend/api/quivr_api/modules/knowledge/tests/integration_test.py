import asyncio
import json
from uuid import UUID

from httpx import AsyncClient

from quivr_api.modules.knowledge.dto.inputs import LinkKnowledgeBrain
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO


async def main():
    url = "http://localhost:5050"
    km_data = {
        "file_name": "test_file.txt",
        "source": "local",
        "is_folder": False,
        "parent_id": None,
    }

    multipart_data = {
        "knowledge_data": (None, json.dumps(km_data), "application/json"),
        "file": ("test_file.txt", b"Test file content", "application/octet-stream"),
    }

    async with AsyncClient(
        base_url=url, headers={"Authorization": "Bearer 123"}
    ) as test_client:
        response = await test_client.post(
            "/knowledge/",
            files=multipart_data,
        )
        response.raise_for_status()
        km = KnowledgeDTO.model_validate(response.json())

        json_data = LinkKnowledgeBrain(
            brain_ids=[UUID("40ba47d7-51b2-4b2a-9247-89e29619efb0")],
            knowledge=km,
        ).model_dump_json()
        response = await test_client.post(
            "/knowledge/link_to_brains/",
            content=json_data,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
