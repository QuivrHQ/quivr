from quivr_api.modules.assistant.services.tasks_service import TasksService
import asyncio
import random


async def process_assistant(assistant_id: str, notification_uuid: str, file1_name_path: str, file2_name_path: str, task_id: int, tasks_service: TasksService):
    
    task = await tasks_service.get_task_by_id(task_id) # type: ignore
    
    await tasks_service.update_task(task_id, {"status": "in_progress"})
    
    print(task)
    
    # Wait for a random time between 10 and 15 seconds
    await asyncio.sleep(random.uniform(10, 15))
    
    task_result = {
        "status": "completed",
        "answer_raw":{
            "text": "#### Assistant answer"
        },
        "answer_pretty": "#### Assistant answer"
    }
    await tasks_service.update_task(task_id, task_result)
    
    
    
    
    
    
    
    
