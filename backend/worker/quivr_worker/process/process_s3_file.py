from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_api.vector.service.vector_service import VectorService
from supabase import Client

from quivr_worker.files import build_file
from quivr_worker.process.process_file import process_file

logger = get_logger("celery_worker")


async def process_uploaded_file(
    supabase_client: Client,
    brain_service: BrainService,
    brain_vector_service: BrainVectorService,
    vector_service: VectorService,
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
    with build_file(file_data, knowledge_id, file_name) as file_instance:
        # TODO(@StanGirard): fix bug
        # NOTE (@aminediro): I think this might be related to knowledge delete timeouts ?
        if delete_file:
            brain_vector_service.delete_file_from_brain(
                file_original_name, only_vectors=True
            )
        await process_file(
            file_instance=file_instance,
            brain=brain,
            brain_service=brain_service,
            brain_vector_service=brain_vector_service,
            vector_service=vector_service,
            integration=integration,
            integration_link=integration_link,
        )
