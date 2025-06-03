Example Python script using [AI/ML API](https://aimlapi.com) with [quivr-core](https://github.com/quivr-ai/quivr) to run LLM-powered prompts.

## Overview

This project demonstrates how to query AI/ML API models (e.g., Gemini, DeepSeek, ChatGPT) via the Quivr agent framework. It includes a basic prompt example and a streaming example.

## Setup

### 1. Clone the repository

### 2. Set up environment

Make sure you have Python 3.11+ installed.

Install the package using pip:

```bash
pip install quivr-core # Check that the installation worked
```

### 3. Set your API key

Insert your API key into the code directly or set it as an environment variable:

```python
llm = ChatOpenAI(
    model='...',
    api_key='***',  # Replace with your AIMLAPI key
    base_url='...',
    max_completion_tokens='...',
    temperature='...',
)
```

> You can get your API key from [aimlapi.com](https://aimlapi.com/?utm_source=quivr&utm_medium=github&utm_campaign=integration)

## Usage

### Basic example

```bash
python simple_question.py
```

### Streaming example

```bash
python simple_question_streaming.py
```
