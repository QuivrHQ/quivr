import os
import random
from io import BytesIO
from tempfile import NamedTemporaryFile

from fastapi import UploadFile
from logger import get_logger
from modules.ingestion.ito.ito import ITO
from modules.upload.controller.upload_routes import upload_file
from openai import OpenAI

logger = get_logger(__name__)


class AudioSummaryIngestion(ITO):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

    async def process_ingestion(self):
        client = OpenAI()

        logger.info(f"Processing audio file {self.uploadFile.filename}")

        # Extract the original filename and create a temporary file with the same name
        filename = os.path.basename(self.uploadFile.filename)
        temp_file = NamedTemporaryFile(delete=False, suffix=filename)

        # Write the uploaded file's data to the temporary file
        data = await self.uploadFile.read()
        temp_file.write(data)
        temp_file.close()

        # Open the temporary file and pass it to the OpenAI API
        with open(temp_file.name, "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=file, response_format="text"
            )
            logger.info(f"Transcription: {transcription}")

            # Delete the temporary file
            os.remove(temp_file.name)

            content_io = BytesIO(transcription.encode("utf-8"))
            content_io.seek(0)

            # Create a file of type UploadFile

            # Generate a new name for the file with self.uploadFile.filename without the extension and add 4 random digits at the end and then .txt
            new_filename = (
                self.uploadFile.filename.split(".")[0]
                + "_audio_summary_"
                + str(random.randint(1000, 9999))
                + ".txt"
            )

            file_to_upload = UploadFile(
                filename=new_filename,
                file=content_io,
                headers={"content-type": "text/plain"},
            )

            if self.send_file_email:
                await self.send_output_by_email(
                    file_to_upload, new_filename, "Summary of the document"
                )
            # Create a file of type UploadFile
            file_to_upload.file.seek(0)
            await upload_file(
                uploadFile=file_to_upload,
                brain_id=self.brain_id,
                current_user=self.current_user,
                chat_id=None,
            )
            return {"message": "Summary generated successfully"}
