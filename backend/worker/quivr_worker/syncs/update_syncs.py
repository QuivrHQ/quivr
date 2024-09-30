from sqlalchemy.ext.asyncio import AsyncEngine

from quivr_worker.utils.services import build_processor_services


async def update_sync_files(async_engine: AsyncEngine):
    async with build_processor_services(async_engine) as processor_services:
        # Get folders
        ## Fetch the folder children
        ##  Fetch all knowledge for this sync
        ## If this knowledge isn't
        ##  Get files
        # Update sync files
        pass


# If knowledge is folder just call the link_knowledge_to_brain
