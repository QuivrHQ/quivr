# Voice Chatbot with Chainlit

This example demonstrates how to create a voice-enabled chatbot using **Quivr** and **Chainlit**. The chatbot lets users upload a text file, ask questions about its content, and interact using speech.

---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **OpenAI API Key**: Ensure you have a valid OpenAI API key.

---

## Installation

1. Clone the repository and navigate to the appropriate directory:
    ```bash
    git clone https://github.com/QuivrHQ/quivr
    cd examples/chatbot_voice
    ```

2. Set the OpenAI API key as an environment variable:
    ```bash
    export OPENAI_API_KEY='<your-key-here>'
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.lock
    ```

---

## Running the Chatbot

1. Start the Chainlit server:
    ```bash
    chainlit run main.py
    ```

2. Open your web browser and navigate to the URL displayed in the terminal (default: `http://localhost:8000`).

---

## Using the Chatbot

### File Upload

1. Once the interface loads, the chatbot will prompt you to upload a `.txt` file.
2. Click on the upload area or drag-and-drop a text file. Ensure the file size is under **20MB**.
3. After processing, the chatbot will notify you that it’s ready for interaction.

### Asking Questions

1. Type your questions in the input box or upload an audio file containing your question.
2. If using text input, the chatbot will respond with an answer derived from the uploaded file's content.
3. If using audio input:
   - The chatbot converts speech to text using OpenAI Whisper.
   - Processes the text query and provides a response.
   - Converts the response to audio, enabling hands-free interaction.

---

## Features

1. **Text File Processing**: Creates a "brain" for the uploaded file using Quivr for question answering.
2. **Speech-to-Text (STT)**: Transcribes user-uploaded audio queries using OpenAI Whisper.
3. **Text-to-Speech (TTS)**: Converts chatbot responses into audio for a seamless voice chat experience.
4. **Source Display**: Shows relevant file sources for each response.
5. **Real-Time Updates**: Uses streaming for live feedback during processing.

---

## How It Works

1. **File Upload**: The user uploads a `.txt` file, which is temporarily saved and processed into a "brain" using Quivr.
2. **Session Handling**: Chainlit manages user sessions to retain the uploaded file and brain context.
3. **Voice Interaction**:
    - Audio queries are processed via the OpenAI Whisper API.
    - Responses are generated and optionally converted into audio for playback.
4. **Streaming**: The chatbot streams its answers incrementally, improving response speed.

---

## Workflow

### Chat Start

1. Waits for a text file upload.
2. Processes the file into a "brain."
3. Notifies the user when ready for interaction.

### On User Message

1. Extracts the "brain" and queries it using the message content.
2. Streams the response back to the user.
3. Displays file sources related to the response.

### Audio Interaction

1. Captures and processes audio chunks during user input.
2. Converts captured audio into text using Whisper.
3. Queries the brain and provides both text and audio responses.

---

Enjoy interacting with your documents in both text and voice modes!