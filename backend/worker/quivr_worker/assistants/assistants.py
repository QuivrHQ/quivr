import os

from quivr_api.modules.assistant.services.tasks_service import TasksService
from quivr_api.modules.upload.service.upload_file import (
    upload_file_storage,
)

from quivr_worker.assistants.cdp_use_case_2 import process_cdp_use_case_2
from quivr_worker.assistants.cdp_use_case_3 import process_cdp_use_case_3
from quivr_worker.utils.pdf_generator.pdf_generator import PDFGenerator, PDFModel


async def process_assistant(
    assistant_id: str,
    notification_uuid: str,
    task_id: int,
    tasks_service: TasksService,
    user_id: str,
):
    print(task_id)
    task = await tasks_service.get_task_by_id(task_id, user_id)  # type: ignore
    assistant_name = task.assistant_name
    output = ""
    if assistant_id == 3:
        print("🤣🤣🤣🤣🤣🤣🤣🤣")
        output = await process_cdp_use_case_3(
            assistant_id, notification_uuid, task_id, tasks_service, user_id
        )
        print(f"Output 🤣: {output}")
    elif assistant_id == 2:
        print("🤣🤣🤣🤣🤣🤣🤣🤣")
        output = await process_cdp_use_case_2(
            assistant_id, notification_uuid, task_id, tasks_service, user_id
        )
        print(f"Output 🤣: {output}")
    else:
        new_task = await tasks_service.update_task(task_id, {"status": "processing"})
    # Add a random delay of 10 to 20 seconds

    print("🔥🔥🔥🔥🔥")
    task_result = {"status": "completed", "answer": output}

    output_dir = f"{assistant_id}/{notification_uuid}"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/output.pdf"

    print("🔥🔥")
    generated_pdf = PDFGenerator(PDFModel(title=assistant_name, content=output))
    generated_pdf.print_pdf()
    generated_pdf.output(output_path)

    print("🔥 upload")
    with open(output_path, "rb") as file:
        await upload_file_storage(file, output_path)

    # Now delete the file
    os.remove(output_path)
    print("🔥🔥🔥")
    await tasks_service.update_task(task_id, task_result)
    print("🔥")
