# Quivr Chatbot Example

This example demonstrates how to create a simple chatbot using Quivr and Chainlit. The chatbot allows users to upload a text file and then ask questions about its content.

## Prerequisites

- Python 3.8 or higher

## Installation

1. Clone the repository or navigate to the `backend/core/examples/chatbot` directory.

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Running the Chatbot

1. Start the Chainlit server:

   ```
   chainlit run main.py
   ```

2. Open your web browser and go to the URL displayed in the terminal (usually `http://localhost:8000`).

## Using the Chatbot

1. When the chatbot interface loads, you will be prompted to upload a text file.

2. Click on the upload area and select a `.txt` file from your computer. The file size should not exceed 20MB.

3. After uploading, the chatbot will process the file and inform you when it's ready.

4. You can now start asking questions about the content of the uploaded file.

5. Type your questions in the chat input and press Enter. The chatbot will respond based on the information in the uploaded file.

## How It Works

The chatbot uses the Quivr library to create a "brain" from the uploaded text file. This brain is then used to answer questions about the file's content. The Chainlit library provides the user interface and handles the chat interactions.

Enjoy chatting with your documents!
