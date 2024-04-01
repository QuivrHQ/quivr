import random
import tempfile
from io import BytesIO
from uuid import UUID

from fastapi import UploadFile
from langchain_community.chat_models import ChatLiteLLM
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.messages import HumanMessage
from logger import get_logger
from modules.upload.controller.upload_routes import upload_file
from modules.user.entity.user_identity import UserIdentity

logger = get_logger(__name__)


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

    async def process_ingestion(self):

        # Create a temporary file with the uploaded file as a temporary file and then pass it to the loader
        tmp_file = tempfile.NamedTemporaryFile(delete=False)

        # Write the file to the temporary file
        tmp_file.write(self.uploadFile.file.read())

        # Now pass the path of the temporary file to the loader

        loader = UnstructuredPDFLoader(tmp_file.name)

        tmp_file.close()

        data = loader.load()

        chat = ChatLiteLLM(model="gpt-3.5-turbo")

        messages = [
            HumanMessage(
                content=f"Summarize the following document. Make it succinct and to the point. Content to summarize: {data[0].page_content}"
            )
        ]
        answer = chat(messages)

        content = answer.content

        # Now create a fake.txt file with the content of the summary with the name of the original file without the extension as an UploadFile object

        content_io = BytesIO(content.encode("utf-8"))

        # Create a file of type UploadFile

        # Generate a new name for the file with self.uploadFile.filename without the extension and add 4 random digits at the end and then .txt
        new_filename = (
            self.uploadFile.filename.split(".")[0]
            + "_summary_"
            + str(random.randint(1000, 9999))
            + ".txt"
        )

        file_to_upload = UploadFile(filename=new_filename, file=content_io)

        # Create a file of type UploadFile
        await upload_file(
            uploadFile=file_to_upload,
            brain_id=self.brain_id,
            current_user=self.current_user,
            chat_id=None,
        )
        return answer.content
