from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.vector.service.vector_service import VectorService

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
        return True
    file_data = supabase_client.storage.from_(bucket_name).download(file_name)

    # TODO: Have the whole logic on do we process file or not
    # Don't process a file that already exists (file_sha1 in the table with STATUS=UPLOADED)
    #
    # - Check on file_sha1 and status
    # - sha1 should be updated at the end
    # If we have some knowledge with error
    # knowledge = await knowledge_service.get_knowledge(knowledge_id=knowledge_id)

    with build_file(file_data, knowledge_id, file_name) as file_instance:
        try:
            await knowledge_service.update_file_sha1_knowledge(
                file_instance.id, file_instance.file_sha1
            )
            # NOTE (@aminediro): I think this might be related to knowledge delete timeouts ?
            await process_file(
                file_instance=file_instance,
                brain=brain,
                brain_service=brain_service,
                vector_service=vector_service,
                integration=integration,
                integration_link=integration_link,
            )

        except FileExistsError:
            logger.error(
                "The content of the knowledge already exists in the brain. Deleting in knowledges and in storage."
            )
            raise FileExistsError(
                "The content of the knowledge already exists in the brain."
            )
