# Voice Chatbot with Flask

This example demonstrates a simple chatbot using **Flask** and **Quivr**, where users can upload a `.txt` file and ask questions based on its content. It supports speech-to-text and text-to-speech capabilities for a seamless interactive experience.

<video style="width:100%" muted="" controls="" alt="type:video">
   <source src="../assets/chatbot_voice_flask.mp4" type="video/mp4">
</video>
---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **OpenAI API Key**: Ensure you have a valid OpenAI API key.

---

## Installation

1. Clone the repository and navigate to the project directory:
    ```bash
    git clone https://github.com/QuivrHQ/quivr
    cd examples/quivr-whisper
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

## Running the Application

1. Start the Flask server:
    ```bash
    python app.py
    ```

2. Open your web browser and navigate to the URL displayed in the terminal (default: `http://localhost:5000`).

---

## Using the Chatbot

### File Upload

1. On the interface, upload a `.txt` file.
2. Ensure the file format is supported and its size is manageable.
3. The file will be processed, and a "brain" instance will be created.

### Asking Questions

1. Use the microphone to record your question (audio upload).
2. The chatbot will process your question and respond with an audio answer.

---

## How It Works

### File Upload
- Users upload a `.txt` file.
- The file is saved to the `uploads` directory and used to create a "brain" using **Quivr**.

### Session Management
- Each session is associated with a unique ID, allowing the system to cache the user's "brain."

### Speech-to-Text
- User audio files are processed with OpenAI's **Whisper** model to generate transcripts.

### Question Answering
- The "brain" processes the transcribed text, retrieves relevant answers, and generates a response.

### Text-to-Speech
- The answer is converted to audio using OpenAI's text-to-speech model and returned to the user.

---

## Workflow

1. **Upload File**:
    - The user uploads a `.txt` file.
    - A "brain" is created and cached for the session.

2. **Ask Questions**:
    - The user uploads an audio file containing a question.
    - The question is transcribed, processed, and answered using the "brain."

3. **Answer Delivery**:
    - The answer is converted to audio and returned to the user as a Base64-encoded string.

---

## Features

1. **File Upload and Processing**:
    - Creates a context-aware "brain" from the uploaded text file.

2. **Audio-based Interaction**:
    - Supports speech-to-text for input and text-to-speech for responses.

3. **Session Management**:
    - Retains user context throughout the interaction.

4. **Integration with OpenAI**:
    - Uses OpenAI models for transcription, answer generation, and audio synthesis.

---

Enjoy interacting with your text files through an intuitive voice-based interface!