import os
from tempfile import NamedTemporaryFile

from logger import get_logger
from modules.assistant.dto.outputs import (
    AssistantOutput,
    InputFile,
    Inputs,
    OutputBrain,
    OutputEmail,
    Outputs,
)
from modules.assistant.ito.ito import ITO
from openai import OpenAI

logger = get_logger(__name__)


class AudioTranscriptAssistant(ITO):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

    async def process_assistant(self):
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

        return await self.create_and_upload_processed_file(
            transcription, self.uploadFile.filename, "Audio Transcript"
        )


def audio_transcript_inputs():
    output = AssistantOutput(
        name="Audio Transcript",
        description="Transcribes an audio file",
        tags=["new"],
        input_description="One audio file to transcribe",
        output_description="Transcription of the audio file",
        inputs=Inputs(
            files=[
                InputFile(
                    key="audio_file",
                    allowed_extensions=["mp3", "wav", "ogg", "m4a"],
                    required=True,
                    description="The audio file to transcribe",
                )
            ]
        ),
        outputs=Outputs(
            brain=OutputBrain(
                required=True,
                description="The brain to which to upload the document",
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
