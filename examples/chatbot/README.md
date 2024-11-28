# Quivr Chatbot Example

This example demonstrates how to create a simple chatbot using Quivr and Chainlit. The chatbot allows users to upload a text file and then ask questions about its content.

## Prerequisites

- Python 3.8 or higher

## Installation

1. Clone the repository and navigate to the `examples/chatbot` directory.

2. Make sure you have [rye](https://rye.astral.sh/) installed.

3. Install the requirements using `rye`:

   ```sh
   rye sync
   ```
4. Activate the venv

   ```sh
   source ./venv/bin/activate
   ```

## Running the Chatbot

1. Define your API key as environment variable. e.g. `export OPENAI_API_KEY=your-key-here`

2. Start the Chainlit server:

   ```
   chainlit run main.py
   ```

3. Open your web browser and go to the URL displayed in the terminal (usually `http://localhost:8000`).

## Using the Chatbot

1. When the chatbot interface loads, you will be prompted to upload a text file.

2. Click on the upload area and select a `.txt` file from your computer. The file size should not exceed 20MB.

3. After uploading, the chatbot will process the file and inform you when it's ready.

4. You can now start asking questions about the content of the uploaded file.

5. Type your questions in the chat input and press Enter. The chatbot will respond based on the information in the uploaded file.

## How It Works

The chatbot uses the Quivr library to create a "brain" from the uploaded text file. This brain is then used to answer questions about the file's content. The Chainlit library provides the user interface and handles the chat interactions.

Enjoy chatting with your documents!
