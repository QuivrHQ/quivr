# Quivr-Whisper

Quivr-Whisper is a web application that allows users to ask questions via audio input. It leverages OpenAI's Whisper model for speech transcription and synthesizes responses using OpenAI's text-to-speech capabilities. The application queries the Quivr API to get a response based on the transcribed audio input.



https://github.com/StanGirard/quivr-whisper/assets/19614572/9cc270c9-07e4-4ce1-bcff-380f195c9313



## Features

- Audio input for asking questions
- Speech transcription using OpenAI's Whisper model
- Integration with Quivr API for intelligent responses
- Speech synthesis of the response for audio playback

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.6+
- pip for Python 3
- Flask
- OpenAI Python package
- Requests package

### Installing

A step by step series of examples that tell you how to get a development environment running:

1. Clone the repository to your local machine.
```bash
git clone https://github.com/stangirard/quivr-whisper.git
cd Quivr-talk
```

2. Install the required packages.
```bash
pip install flask openai requests python-dotenv
```

3. Create a `.env` file in the root directory of the project and add your API keys and other configuration variables.
```env
OPENAI_API_KEY='your_openai_api_key'
QUIVR_API_KEY='your_quivr_api_key'
QUIVR_CHAT_ID='your_quivr_chat_id'
QUIVR_BRAIN_ID='your_quivr_brain_id'
QUIVR_URL='https://api.quivr.app' # Optional, only if different from the default
```

4. Run the Flask application.
```bash
flask run
```

Your app should now be running on `http://localhost:5000`.

## Usage

To use Quivr-talk, navigate to `http://localhost:5000` in your web browser, click on "Ask a question to Quivr", and record your question. Wait for the transcription and response to be synthesized, and you will hear the response played back to you.
