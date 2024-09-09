from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.brain.service.brain_service import BrainService
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
    brain_id: UUID,
    file_original_name: str,
    knowledge_id: UUID,
    integration: str | None = None,
    integration_link: str | None = None,
    delete_file: bool = False,
    bucket_name: str = "quivr",
):
    brain = brain_service.get_brain_by_id(brain_id)
    if brain is None:
        logger.exception(
            "It seems like you're uploading knowledge to an unknown brain."
        )
        raise ValueError("unknown brain")
    assert brain
    file_data = supabase_client.storage.from_(bucket_name).download(file_name)
    # TODO: Have the whole logic on do we process file or not
    # Don't process a file that already exists (file_sha1 in the table with STATUS=UPLOADED)
    #
    # - Check on file_sha1 and status
    # If we have some knowledge with error
    with build_file(file_data, knowledge_id, file_name) as file_instance:
        knowledge = await knowledge_service.get_knowledge(knowledge_id=knowledge_id)
        should_process = await knowledge_service.update_sha1_conflict(
            knowledge=knowledge,
            brain_id=brain.brain_id,
            file_sha1=file_instance.file_sha1,
        )
        if should_process:
            await process_file(
                file_instance=file_instance,
                brain=brain,
                brain_service=brain_service,
                vector_service=vector_service,
                integration=integration,
                integration_link=integration_link,
            )
