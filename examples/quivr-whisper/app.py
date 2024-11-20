from flask import Flask, render_template, request, jsonify
import openai
import base64
import os
import requests
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile

app = Flask(__name__)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

quivr_token = os.getenv("QUIVR_API_KEY", "")
quivr_chat_id = os.getenv("QUIVR_CHAT_ID", "")
quivr_brain_id = os.getenv("QUIVR_BRAIN_ID", "")
quivr_url = (
    os.getenv("QUIVR_URL", "https://api.quivr.app")
    + f"/chat/{quivr_chat_id}/question?brain_id={quivr_brain_id}"
)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {quivr_token}",
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    audio_file = request.files["audio_data"]
    transcript = transcribe_audio_file(audio_file)
    quivr_response = ask_quivr_question(transcript)
    audio_base64 = synthesize_speech(quivr_response)
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


def ask_quivr_question(transcript):
    response = requests.post(quivr_url, headers=headers, json={"question": transcript})
    if response.status_code == 200:
        quivr_response = response.json().get("assistant")
        return quivr_response
    else:
        print(f"Error from Quivr API: {response.status_code}, {response.text}")
        return "Sorry, I couldn't understand that."


def synthesize_speech(text):
    speech_response = openai.audio.speech.create(
        model="tts-1", voice="nova", input=text
    )
    audio_content = speech_response.content
    audio_base64 = base64.b64encode(audio_content).decode("utf-8")
    return audio_base64


if __name__ == "__main__":
    app.run(debug=True)
