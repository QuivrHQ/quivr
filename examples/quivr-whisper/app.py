from flask import Flask, render_template, request, jsonify, session
import openai
import base64
import os
import requests
from dotenv import load_dotenv
from quivr_core import Brain
from quivr_core.rag.entities.config import RetrievalConfig
from tempfile import NamedTemporaryFile
from werkzeug.utils import secure_filename
from asyncio import to_thread
import asyncio


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "secret"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CACHE_TYPE"] = "SimpleCache"  # In-memory cache for development
app.config["CACHE_DEFAULT_TIMEOUT"] = 60 * 60  # 1 hour cache timeout
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

brains = {}


@app.route("/")
def index():
    return render_template("index.html")


def run_in_event_loop(func, *args, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if asyncio.iscoroutinefunction(func):
        result = loop.run_until_complete(func(*args, **kwargs))
    else:
        result = func(*args, **kwargs)
    loop.close()
    return result


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
async def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400
    if not (file and file.filename and allowed_file(file.filename)):
        return "Invalid file type", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    print(f"File uploaded and saved at: {filepath}")

    print("Creating brain instance...")

    brain: Brain = await to_thread(
        run_in_event_loop, Brain.from_files, name="user_brain", file_paths=[filepath]
    )

    # Store brain instance in cache
    session_id = session.sid if hasattr(session, "sid") else os.urandom(16).hex()
    session["session_id"] = session_id
    # cache.set(session_id, brain)  # Store the brain instance in the cache
    brains[session_id] = brain
    print(f"Brain instance created and stored in cache for session ID: {session_id}")

    return jsonify({"message": "Brain created successfully"})


@app.route("/ask", methods=["POST"])
async def ask():
    if "audio_data" not in request.files:
        return "Missing audio data", 400

    # Retrieve the brain instance from the cache using the session ID
    session_id = session.get("session_id")
    if not session_id:
        return "Session ID not found. Upload a file first.", 400

    brain = brains.get(session_id)
    if not brain:
        return "Brain instance not found in dict. Upload a file first.", 400

    print("Brain instance loaded from cache.")

    print("Speech to text...")
    audio_file = request.files["audio_data"]
    transcript = transcribe_audio_file(audio_file)
    print("Transcript result: ", transcript)

    print("Getting response...")
    quivr_response = await to_thread(run_in_event_loop, brain.ask, transcript)

    print("Text to speech...")
    audio_base64 = synthesize_speech(quivr_response.answer)

    print("Done")
    return jsonify({"audio_base64": audio_base64})


def transcribe_audio_file(audio_file):
    with NamedTemporaryFile(suffix=".webm", delete=False) as temp_audio_file:
        audio_file.save(temp_audio_file)
        temp_audio_file_path = temp_audio_file.name

    try:
        with open(temp_audio_file_path, "rb") as f:
            transcript_response = openai.audio.transcriptions.create(
                model="whisper-1", file=f
            )
        transcript = transcript_response.text
    finally:
        os.unlink(temp_audio_file_path)

    return transcript


def synthesize_speech(text):
    speech_response = openai.audio.speech.create(
        model="tts-1", voice="nova", input=text
    )
    audio_content = speech_response.content
    audio_base64 = base64.b64encode(audio_content).decode("utf-8")
    return audio_base64


if __name__ == "__main__":
    app.run(debug=True)
