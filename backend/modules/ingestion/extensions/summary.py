import tempfile
from uuid import UUID

from fastapi import UploadFile
from langchain_community.chat_models import ChatLiteLLM
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.messages import HumanMessage
from modules.user.entity.user_identity import UserIdentity


class SummaryIngestion:
    uploadFile: UploadFile = None
    current_user: UserIdentity = None
    brain_id: UUID = None

    def __init__(
        self, uploadFile: UploadFile, current_user: UserIdentity, brain_id: UUID
    ):
        self.uploadFile = uploadFile
        self.current_user = current_user
        self.brain_id = brain_id

    def process_ingestion(self):

        # Create a temporary file with the uploaded file as a temporary file and then pass it to the loader
        tmp_file = tempfile.NamedTemporaryFile(delete=False)

        # Write the file to the temporary file
        tmp_file.write(self.uploadFile.file.read())

        # Now pass the path of the temporary file to the loader

        loader = UnstructuredPDFLoader(tmp_file.name)

        data = loader.load()

        chat = ChatLiteLLM(model="gpt-3.5-turbo")

        messages = [
            HumanMessage(
                content=f"Summarize the following document. Make it succinct and to the point. Content to summarize: {data[0].page_content}"
            )
        ]
        answer = chat(messages)

        return answer.content
