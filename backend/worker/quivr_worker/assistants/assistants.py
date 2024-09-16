from quivr_api.modules.assistant.services.tasks_service import TasksService
import asyncio
import random
from quivr_worker.utils.pdf_generator.pdf_generator import PDFGenerator, PDFModel
from quivr_api.modules.upload.service.upload_file import (
    upload_file_storage,
)
import os

async def process_assistant(assistant_id: str, notification_uuid: str, file1_name_path: str, file2_name_path: str, task_id: int, tasks_service: TasksService):
    
    task = await tasks_service.get_task_by_id(task_id) # type: ignore
    
    await tasks_service.update_task(task_id, {"status": "in_progress"})
    
    print(task)
    

    
    task_result = {
        "status": "completed",
        "answer_raw":{
            "text": "#### Assistant answer"
        },
        "answer_pretty": "#### Assistant answer"
    }
    
    generated_pdf = PDFGenerator(PDFModel(title="Test", content="Test"))
    generated_pdf.print_pdf()
    generated_pdf.output(f"{assistant_id}/{notification_uuid}/output.pdf")
    
    with open(f"{assistant_id}/{notification_uuid}/output.pdf", "rb") as file:
        await upload_file_storage(file, f"{assistant_id}/{notification_uuid}/output.pdf")
    
    # Now delete the file
    os.remove(f"{assistant_id}/{notification_uuid}/output.pdf")
    
    
    await tasks_service.update_task(task_id, task_result)
    
    
    
    
    
    
    
    
