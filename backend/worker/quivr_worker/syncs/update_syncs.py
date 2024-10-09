from sqlalchemy.ext.asyncio import AsyncEngine

from quivr_worker.process.processor import KnowledgeProcessor
from quivr_worker.utils.services import build_processor_services


async def refresh_sync_files(async_engine: AsyncEngine):
    async with build_processor_services(async_engine) as processor_services:
        km_processor = KnowledgeProcessor(services=processor_services)
        await km_processor.refresh_knowledge_sync_files()


async def refresh_sync_folders(async_engine: AsyncEngine):
    async with build_processor_services(async_engine) as processor_services:
        km_processor = KnowledgeProcessor(services=processor_services)
        await km_processor.refresh_knowledge_sync_files()
