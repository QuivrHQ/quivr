from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.knowledge.dto.inputs import KnowledgeUpdate
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.vector.service.vector_service import VectorService

from quivr_worker.files import build_file
from quivr_worker.process.process_file import process_file
from supabase import Client

logger = get_logger("celery_worker")


async def process_uploaded_file(
    supabase_client: Client,
    brain_service: BrainService,
    vector_service: VectorService,
    knowledge_service: KnowledgeService,
    file_name: str,
    knowledge_id: UUID,
    integration: str | None = None,
    integration_link: str | None = None,
    bucket_name: str = "quivr",
):
    file_data = supabase_client.storage.from_(bucket_name).download(file_name)
    with build_file(file_data, knowledge_id, file_name) as file_instance:
        knowledge = await knowledge_service.get_knowledge(knowledge_id=knowledge_id)
        await knowledge_service.update_knowledge(
            knowledge,
            KnowledgeUpdate(file_sha1=file_instance.file_sha1),  # type: ignore
        )
        await process_file(
            file_instance=file_instance,
            brain=knowledge.brains[0],  # FIXME: this is temporary
            brain_service=brain_service,
            vector_service=vector_service,
            integration=integration,
            integration_link=integration_link,
        )
