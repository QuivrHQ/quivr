import os

from quivr_api.modules.assistant.services.tasks_service import TasksService
from quivr_api.modules.upload.service.upload_file import (
    upload_file_storage,
)

from quivr_worker.utils.pdf_generator.pdf_generator import PDFGenerator, PDFModel


async def process_assistant(
    assistant_id: str,
    notification_uuid: str,
    task_id: int,
    tasks_service: TasksService,
    user_id: str,
):
    task = await tasks_service.get_task_by_id(task_id, user_id)  # type: ignore

    await tasks_service.update_task(task_id, {"status": "in_progress"})

    print(task)

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
