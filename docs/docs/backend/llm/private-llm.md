---
sidebar_position: 1
---

# Private LLM

Quivr now has the capability to use a private LLM model powered by GPT4All (other open source models coming soon).

This is similar to the functionality provided by the PrivateGPT project.

This means that your data never leaves the server. The LLM is downloaded to the server and runs inference on your question locally.

## How to use

Set the 'private' flag to True in the /backend/.env file. You can also set other model parameters in the .env file.

Download the GPT4All model from [here](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin) and place it in the /backend/local_models folder. Or you can download any model from their ecosystem on their [website](https://gpt4all.io/index.html).

## Future Plans

We are planning to add more models to the private LLM feature. We are also planning on using a local embedding model from Hugging Face to reduce our reliance on OpenAI's API.

We will also be adding the ability to use a private LLM model from the frontend and api. Currently it is only available if you self host the backend.
