import tempfile
import os
import chainlit as cl
from quivr_core import Brain
from quivr_core.rag.entities.config import RetrievalConfig
from openai import AsyncOpenAI
from chainlit.element import Element

from io import BytesIO


@cl.on_chat_start
async def on_chat_start():
    files = None

    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a text .txt file to begin!",
            accept=["text/plain"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]

    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()

    with open(file.path, "r", encoding="utf-8") as f:
        text = f.read()

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=file.name, delete=False
    ) as temp_file:
        temp_file.write(text)
        temp_file.flush()
        temp_file_path = temp_file.name

    brain = Brain.from_files(name="user_brain", file_paths=[temp_file_path])

    # Store the file path in the session
    cl.user_session.set("file_path", temp_file_path)

    # Let the user know that the system is ready
    msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    await msg.update()

    cl.user_session.set("brain", brain)


@cl.on_message
async def main(message: cl.Message):

    task_list = cl.TaskList(name="State")
    task_list.status = "Running..."

    think = cl.Task(title="Thinking", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(think)

    tts = cl.Task(title="Text to speech")
    await task_list.add_task(tts)

    await task_list.send()

    brain = cl.user_session.get("brain")  # type: Brain
    path_config = "basic_rag_workflow.yaml"
    retrieval_config = RetrievalConfig.from_yaml(path_config)

    if brain is None:
        await cl.Message(content="Please upload a file first.").send()
        return

    # Prepare the message for streaming
    msg = cl.Message(content="", elements=[], author="Quivr", type="assistant_message")
    await msg.send()

    saved_sources = set()
    saved_sources_complete = []
    elements = []

    # Use the ask_stream method for streaming responses
    async for chunk in brain.ask_streaming(message.content, retrieval_config=retrieval_config):
        await msg.stream_token(chunk.answer)
        for source in chunk.metadata.sources:
            if source.page_content not in saved_sources:
                saved_sources.add(source.page_content)
                saved_sources_complete.append(source)
                print(source)
                elements.append(cl.Text(name=source.metadata["original_file_name"], content=source.page_content, display="side"))
    
    think.status = cl.TaskStatus.DONE
    tts.status = cl.TaskStatus.RUNNING
    await task_list.update()
    
    audio_file = await text_to_speech(msg.content)
    elements.append(cl.Audio(content=audio_file, auto_play=True, mime="audio/mpeg"))

    sources = ""
    for source in saved_sources_complete:
        sources += f"- {source.metadata['original_file_name']}\n"
    msg.elements = elements
    msg.content = msg.content + f"\n\nSources:\n{sources}"
    await msg.update()

    tts.status = cl.TaskStatus.DONE
    task_list.status = "Done"
    await task_list.update()
    await cl.sleep(1)
    await task_list.remove()

async_openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@cl.step(type="tool", name="Speech to text")
async def speech_to_text(audio_file):
    response = await async_openai_client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )

    return response.text

@cl.step(type="tool", name="Text to speech")
async def text_to_speech(text):
    response = await async_openai_client.audio.speech.create(
        model="tts-1", voice="alloy", input=text
    )

    return response.content


@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.AudioChunk):
    if chunk.isStart:
        buffer = BytesIO()
        # This is required for whisper to recognize the file type
        buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
        # Initialize the session for a new audio stream
        cl.user_session.set("audio_buffer", buffer)
        cl.user_session.set("audio_mime_type", chunk.mimeType)

    # Write the chunks to a buffer and transcribe the whole audio at the end
    cl.user_session.get("audio_buffer").write(chunk.data)


@cl.on_audio_end
async def on_audio_end(elements: list[Element]):
    # Get the audio buffer from the session
    task_list = cl.TaskList(name="State")
    task_list.status = "Running..."

    stt = cl.Task(title="Speech to text", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(stt)

    await task_list.send()

    audio_buffer: BytesIO = cl.user_session.get("audio_buffer")
    audio_buffer.seek(0)  # Move the file pointer to the beginning
    audio_file = audio_buffer.read()
    audio_mime_type: str = cl.user_session.get("audio_mime_type")

    input_audio_el = cl.Audio(
        mime=audio_mime_type, content=audio_file, name=audio_buffer.name
    )
    await cl.Message(
        author="You",
        type="user_message",
        content="",
        elements=[input_audio_el, *elements],
    ).send()

    whisper_input = (audio_buffer.name, audio_file, audio_mime_type)
    transcription = await speech_to_text(whisper_input)

    msg = cl.Message(author="You", content=transcription, elements=elements)

    stt.status = cl.TaskStatus.DONE
    task_list.status = "Done"
    await task_list.update()
    await cl.sleep(1)
    await task_list.remove()

    await main(message=msg)