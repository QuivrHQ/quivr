# Chatbot with Chainlit

This example demonstrates a simple chatbot using **Quivr** and **Chainlit**, where users can upload a `.txt` file and ask questions based on its content.

---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **OpenAI API Key**: Ensure you have a valid OpenAI API key.

---

## Installation

1. Clone the repository and navigate to the appropriate directory:
    ```bash
    git clone https://github.com/QuivrHQ/quivr
    cd examples/chatbot
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

1. On the chatbot interface, upload a `.txt` file when prompted.
2. Ensure the file size is under **20MB**.
3. After uploading, the file is processed, and you will be notified when the chatbot is ready.

### Asking Questions

1. Type your questions into the chat input and press Enter.
2. The chatbot will respond based on the content of the uploaded file.
3. Relevant file sources for the answers are displayed in the chat.

---

## How It Works

1. **File Upload**:
    - Users upload a `.txt` file, which is temporarily saved.
    - The chatbot processes the file using Quivr to create a "brain."

2. **Session Handling**:
    - Chainlit manages the session to retain the file path and brain context.

3. **Question Answering**:
    - The chatbot uses the `ask_streaming` method from Quivr to process user queries.
    - Responses are streamed incrementally for faster feedback.
    - Relevant file excerpts (sources) are extracted and displayed.

4. **Retrieval Configuration**:
    - A YAML file (`basic_rag_workflow.yaml`) defines retrieval parameters for Quivr.

---

## Workflow

### Chat Start

1. Waits for the user to upload a `.txt` file.
2. Processes the file and creates a "brain."
3. Notifies the user when the system is ready for questions.

### On User Message

1. Retrieves the "brain" from the session.
2. Processes the user's question with Quivr.
3. Streams the response and displays it in the chat.
4. Extracts and shows relevant sources from the file.

---

## Features

1. **File Processing**: Creates a context-aware "brain" from the uploaded file.
2. **Streaming Responses**: Delivers answers incrementally for better user experience.
3. **Source Highlighting**: Displays file excerpts relevant to the answers.

---

Enjoy interacting with your text files in a seamless Q&A format!