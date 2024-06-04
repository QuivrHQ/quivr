from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.pydantic_v1 import BaseModel as BaseModelV1
from langchain.pydantic_v1 import Field as FieldV1
from langchain.tools import BaseTool
from langchain_core.tools import BaseTool
from openai import OpenAI
from pydantic import BaseModel


class ImageGenerationInput(BaseModelV1):
    query: str = FieldV1(
        ...,
        title="description",
        description="A detailled prompt to generate the image from. Takes into account the history of the chat.",
    )


class ImageGeneratorTool(BaseTool):
    name = "image-generator"
    description = "useful for when you need to generate an image from a prompt."
    args_schema: Type[BaseModel] = ImageGenerationInput
    return_direct = True

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        client = OpenAI()

        response = client.images.generate(
            model="dall-e-3",
            prompt=query,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt
        # Make the url a markdown image
        return f"{revised_prompt} \n ![Generated Image]({image_url}) "

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        client = OpenAI()
        response = await run_manager.run_async(
            client.images.generate,
            model="dall-e-3",
            prompt=query,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt
        # Make the url a markdown image
        return f"{revised_prompt} \n ![Generated Image]({image_url}) "
