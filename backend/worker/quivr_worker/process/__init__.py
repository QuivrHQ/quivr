from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncEngine

from quivr_worker.process.processor import KnowledgeProcessor
from quivr_worker.utils.services import build_processor_services


async def aprocess_file_task(async_engine: AsyncEngine, knowledge_id: UUID):
    async with build_processor_services(async_engine) as processor_services:
        km_processor = KnowledgeProcessor(services=processor_services)
        await km_processor.process_knowledge(knowledge_id)
