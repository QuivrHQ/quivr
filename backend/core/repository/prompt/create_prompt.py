from models.prompt import Prompt
from models.settings import common_dependencies
from pydantic import BaseModel


class CreatePromptProperties(BaseModel):
    """Properties that can be received on prompt creation"""

    title: str
    content: str
    status: str = "private"


def create_prompt(prompt: CreatePromptProperties) -> Prompt:
    """Create a prompt by id"""
    commons = common_dependencies()

    response = (
        commons["supabase"].from_("prompts").insert(prompt.dict()).execute()
    ).data

    return Prompt(**response[0])
