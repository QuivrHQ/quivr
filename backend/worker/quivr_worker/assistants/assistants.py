import os

from quivr_api.modules.assistant.repository.tasks import TasksRepository
from quivr_api.modules.assistant.services.tasks_service import TasksService
from quivr_api.modules.upload.service.upload_file import (
    upload_file_storage,
)
from sqlalchemy.ext.asyncio import AsyncEngine

from quivr_worker.utils.pdf_generator.pdf_generator import PDFGenerator, PDFModel
from quivr_worker.utils.services import _start_session


async def aprocess_assistant_task(
    engine: AsyncEngine,
    assistant_id: str,
    notification_uuid: str,
    task_id: int,
    user_id: str,
):
    async with _start_session(engine) as async_session:
        try:
            tasks_repository = TasksRepository(async_session)
            tasks_service = TasksService(tasks_repository)

            await process_assistant(
                assistant_id,
                notification_uuid,
                task_id,
                tasks_service,
                user_id,
            )

        except Exception as e:
            await async_session.rollback()
            raise e
        finally:
            await async_session.close()


async def process_assistant(
    assistant_id: str,
    notification_uuid: str,
    task_id: int,
    tasks_service: TasksService,
    user_id: str,
):
    task = await tasks_service.get_task_by_id(task_id, user_id)  # type: ignore
    assert task.id
    await tasks_service.update_task(task.id, {"status": "in_progress"})

    task_result = {"status": "completed", "answer": "#### Assistant answer"}

    output_dir = f"{assistant_id}/{notification_uuid}"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/output.pdf"

    generated_pdf = PDFGenerator(PDFModel(title="Test", content="Test"))
    generated_pdf.print_pdf()
    generated_pdf.output(output_path)

    with open(output_path, "rb") as file:
        await upload_file_storage(file, output_path)

    # Now delete the file
    os.remove(output_path)

    await tasks_service.update_task(task_id, task_result)
