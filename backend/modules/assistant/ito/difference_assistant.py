import asyncio
import os
import tempfile
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import List

import httpx
import pandas as pd
from fastapi import UploadFile
from logger import get_logger
from megaparse.Converter import MegaParse
from modules.assistant.dto.inputs import InputAssistant
from modules.assistant.dto.outputs import (
    AssistantOutput,
    InputFile,
    Inputs,
    OutputBrain,
    OutputEmail,
    Outputs,
)
from modules.assistant.ito.difference.difference_agent import ContextType
from modules.assistant.ito.ito import ITO

# from modules.upload.controller.upload_routes import upload_file #FIXME circular import
from modules.user.entity.user_identity import UserIdentity

from .difference import DifferenceAgent, DiffQueryEngine

logger = get_logger(__name__)


# FIXME: PATCHER -> find another solution
async def upload_file_to_api(upload_file, brain_id, current_user):
    url = "http://localhost:5050/upload"
    headers = {
        "Authorization": f"Bearer {current_user.token}",
        "Content-Type": "application/json",
    }
    data = {
        "uploadFile": upload_file,
        "brain_id": brain_id,
        "chat_id": None,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for 4xx/5xx responses
        return response.json()


class DifferenceAssistant(ITO):

    def __init__(
        self,
        input: InputAssistant,
        files: List[UploadFile] = None,  # type: ignore
        current_user: UserIdentity = None,  # type: ignore
        **kwargs,
    ):
        super().__init__(
            input=input,
            files=files,
            current_user=current_user,
            **kwargs,
        )

    def check_input(self):
        if not self.files:
            raise ValueError("No file was uploaded")
        if len(self.files) != 2:
            raise ValueError("Only two files can be uploaded")
        if not self.input.inputs.files:
            raise ValueError("No files key were given in the input")
        if len(self.input.inputs.files) != 2:
            raise ValueError("Only two files can be uploaded")
        if not self.input.inputs.files[0].key == "ref_doc":
            raise ValueError("The key of the first file should be ref_doc")
        if not self.input.inputs.files[1].key == "target_doc":
            raise ValueError("The key of the second file should be target_doc")
        if not self.input.inputs.files[0].value:
            raise ValueError("No file was uploaded")
        if not (
            self.input.outputs.brain.activated or self.input.outputs.email.activated  # type: ignore
        ):
            raise ValueError("No output was selected")
        return True

    async def process_assistant(self):
        print("\nRunning Difference Assistant\n")
        tab_name = ""
        category = ""

        for elements in self.input.inputs.texts:  # type: ignore
            if elements.key == "tab_name":
                tab_name = elements.value
            elif elements.key == "category":
                category = elements.value
        print("tab name: ", tab_name, "category : ", category)

        # breakpoint()

        ## Process the documents
        ##----------------------
        document_1 = self.files[0]
        document_2 = self.files[1]

        # Get the file extensions
        document_1_ext = os.path.splitext(document_1.filename)[1]  # type: ignore
        document_2_ext = os.path.splitext(document_2.filename)[1]  # type: ignore

        # Create temporary files with the same extension as the original files
        document_1_tmp = tempfile.NamedTemporaryFile(
            suffix=document_1_ext, delete=False
        )
        document_2_tmp = tempfile.NamedTemporaryFile(
            suffix=document_2_ext, delete=False
        )

        document_1_tmp.write(document_1.file.read())
        document_2_tmp.write(document_2.file.read())

        print("\nRoad to MegaParse, currently parsing the documents\n")
        print(document_1_tmp.name)
        print(document_2_tmp.name)

        for key in self.input.inputs.files:  # type: ignore
            if key.key == "ref_doc":
                ref_doc_name = key.value
            elif key.key == "target_doc":
                target_doc_name = key.value

        print(target_doc_name, "\n")
        print(ref_doc_name, "\n")

        def run_megaparse():
            megaparse = MegaParse(
                file_path=document_1_tmp.name,
                llama_parse_api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
            )
            return megaparse.convert(gpt4o_cleaner=True)

        # breakpoint()
        try:
            megaparse = MegaParse(
                file_path=document_1_tmp.name,
                llama_parse_api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
            )
            loop = asyncio.get_event_loop()
            executor = ThreadPoolExecutor(max_workers=1)
            ref_doc_md = await loop.run_in_executor(executor, run_megaparse)  # type: ignore
            # ref_doc_md = megaparse.convert(gpt4o_cleaner=True)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

            raise ValueError("Error parsing the reference document")

        additional_context = ContextType(
            category=category,
            context=f"pour les produits de la catégorie {category} ?",
        )

        # FIXME: Add a check if the pkl name file already exists before launching megaparse
        megaparse = MegaParse(file_path=document_2_tmp.name)
        target_doc_md = megaparse.convert_tab(tab_name=tab_name)  # type: ignore
        ##----------------------
        ref_doc_md = [ref_doc_md]
        target_doc_md = [target_doc_md]

        print("\nDocuments parsed successfully\n")

        ## Create diff_query_engine
        ##----------------------
        diff_query_engine = DiffQueryEngine(ref_doc_md, 15)  # type: ignore
        ##----------------------

        DOCUMENT_CONTEXT = None  # type: ignore

        print("\nCreating the Difference Agent\n")
        ## Create the Difference Agent
        ##----------------------
        agent = DifferenceAgent(diff_query_engine)
        print("\nDifference Agent created successfully, generating questions ...\n")
        questions = agent.generate_questions(
            target_content=target_doc_md[0], language_verification=True
        )

        print("\nQuestions generated successfully, asking questions to Quivr\n")

        diff_df = pd.DataFrame()

        diff_df = await agent.run(additional_context=additional_context)

        diff_df = diff_df.dropna()
        print("\nNice, the process has succeeded, giving back the json ;)\n")

        content = generate_authorisation_report(diff_df)

        original_filename = "Classic Ingredient Comparison"
        file_description = "Difference Report"
        processed_file = self.create_and_upload_processed_file(
            content,
            original_filename=original_filename,
            file_description=file_description,
        )  # FIXME change name
        file_to_upload = processed_file["file_to_upload"]
        new_filename = processed_file["new_filename"]

        # Email the file if required
        if self.input.outputs.email.activated:
            await self.send_output_by_email(
                file_to_upload,
                new_filename,
                "Difference",
                f"{file_description} of {original_filename}",
                brain_id=(
                    self.input.outputs.brain.value
                    if self.input.outputs.brain.activated
                    and self.input.outputs.brain.value
                    else None
                ),
            )

        # Reset to start of file before upload
        file_to_upload.file.seek(0)

        # Upload the file if required
        if self.input.outputs.brain.activated:
            response = await upload_file_to_api(
                upload_file=file_to_upload,
                brain_id=self.input.outputs.brain.value,
                current_user=self.current_user,
            )

        return {"message": f"{file_description} generated successfully"}


def generate_authorisation_report(df: pd.DataFrame):
    # Ensure the dataframe has the required columns
    if "name" not in df.columns or "decision" not in df.columns:
        raise ValueError("DataFrame must contain 'name' and 'decision' columns")

    # Extract forbidden and to avoid ingredients
    forbidden_ingredients = df[df["decision"] == "Forbidden"][
        ["name", "detailed_answer"]
    ].values.tolist()
    to_avoid_ingredients = df[df["decision"] == "To Avoid"][
        ["name", "detailed_answer"]
    ].values.tolist()

    # Create the markdown content
    markdown_content = "# Coup de Pates\n\n"
    markdown_content += "## Rapport d'analyse\n\n"

    if forbidden_ingredients:
        markdown_content += "### Ingrédients utilisés **Interdits**\n\n"
        for ingredient, detail in forbidden_ingredients:
            markdown_content += f"**{ingredient}**: *{detail}*\n\n"
    else:
        markdown_content += "### Ingrédients utilisés **Interdits**\n- Aucun\n\n"

    markdown_content += "\n"

    if to_avoid_ingredients:
        markdown_content += "### Ingrédients utilisés **à éviter**\n"
        for ingredient, detail in to_avoid_ingredients:
            markdown_content += f"**{ingredient}** : *{detail}*\n\n"
    else:
        markdown_content += "### To Avoid Ingredients\n- None\n\n"

    return markdown_content


def difference_inputs():
    output = AssistantOutput(
        name="difference",
        description="Finds the difference between two sets of documents",
        tags=["new"],
        input_description="Two documents to compare",
        output_description="The difference between the two documents",
        icon_url="https://quivr-cms.s3.eu-west-3.amazonaws.com/report_94bea8b918.png",
        inputs=Inputs(
            files=[
                InputFile(
                    key="ref_doc",
                    allowed_extensions=["pdf"],
                    required=True,
                    description="The reference document",
                ),
                InputFile(
                    key="target_doc",
                    allowed_extensions=["pdf", "xlsx"],
                    required=True,
                    description="The target document to compare to the reference document.",
                ),
            ],
        ),
        outputs=Outputs(
            brain=OutputBrain(
                required=True,
                description="The brain to which upload the document",
                type="uuid",
            ),
            email=OutputEmail(
                required=True,
                description="Send the document by email",
                type="str",
            ),
        ),
    )
    return output
