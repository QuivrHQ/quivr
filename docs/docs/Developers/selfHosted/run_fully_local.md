---
sidebar_position: 2
title: Run Quivr fully locally
---

# Using Quivr fully locally

## Headers

The following is a guide to set up everything for using Quivr locally:

##### Table of Contents

- [Database](#database)
- [Embeddings](#embeddings)
- [LLM for inference](#llm)

It is a first, working setup, but a lot of work has to be done to e.g. find the appropriate settings for the model.

Importantly, this will currently only work on tag v0.0.46.

The guide was put together in collaboration with members of the Quivr Discord, **Using Quivr fully locally** thread. That is a good place to discuss it.

This worked for me, but I sometimes got strange results (the output contains repeating answers/questions). Maybe because `stopping_criteria=stopping_criteria` must be uncommented in `transformers.pipeline`. Will update this page as I continue learning.

<a name="database"/>

## Local Supabase

Instead of relying on a remote Supabase instance, we have to set it up locally. Follow the instructions on https://supabase.com/docs/guides/self-hosting/docker.

Troubleshooting:

- If the Quivr backend container cannot reach Supabase on port 8000, change the Quivr backend container to use the host network.
- If email service does not work, add a user using the supabase web ui, and check "Auto Confirm User?".
  - http://localhost:8000/project/default/auth/users

<a name="embeddings"/>

## Local embeddings

First, let's get local embeddings to work with GPT4All. Instead of relying on OpenAI for generating embeddings of both the prompt and the documents we upload, we will use a local LLM for this.

Remove any existing data from the postgres database:

- `supabase/docker $ docker compose down -v`
- `supabase/docker $ rm -rf volumes/db/data/`
- `supabase/docker $ docker compose up -d`

Change the vector dimensions in the necessary Quivr SQL files:

- Replace all occurrences of 1536 by 768, in Quivr's `scripts\tables.sql`
- Run tables.sql in the Supabase web ui SQL editor: http://localhost:8000

Change the Quivr code to use local LLM (GPT4All) and local embeddings:

- add code to `backend\core\llm\private_gpt4all.py`

```python
    from langchain.embeddings import HuggingFaceEmbeddings
    ...
    def embeddings(self) -> HuggingFaceEmbeddings:
        emb = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cuda'},
            encode_kwargs={'normalize_embeddings': False}
        )
        return emb
```

Note that there may be better models out there for generating the embeddings: https://huggingface.co/spaces/mteb/leaderboard

Update Quivr `backend/core/.env`'s Private LLM Variables:

```
    #Private LLM Variables
    PRIVATE=True
    MODEL_PATH=./local_models/ggml-gpt4all-j-v1.3-groovy.bin
```

Download GPT4All model:

- `$ cd backend/core/local_models/`
- `wget https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin`

Ensure the Quivr backend docker container has CUDA and the GPT4All package:

```
    FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel
    #FROM python:3.11-bullseye

    ARG DEBIAN_FRONTEND=noninteractive
    ENV DEBIAN_FRONTEND=noninteractive

    RUN pip install gpt4all
```

Modify the docker-compose yml file (for backend container). The following example is for using 2 GPUs:

```
    ...
    network_mode: host
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 2
              capabilities: [gpu]
```

Install nvidia container toolkit on the host, https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html:

```
$ wget https://nvidia.github.io/nvidia-docker/gpgkey --no-check-certificate
$ sudo apt-key add gpgkey
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
$ curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
$ sudo apt-get update

$ sudo apt-get install -y nvidia-container-toolkit

$ nvidia-ctk --version

$ sudo systemctl restart docker
```

At this moment, if we try to upload a pdf, we get an error:

```
backend-core  | 1989-01-01 21:51:41,211 [ERROR] utils.vectors: Error creating vector for document {'code': '22000', 'details': None, 'hint': None, 'message': 'expected 768 dimensions, not 1536'}
```

This can be remedied by using local embeddings for document embeddings. In backend/core/utils/vectors.py, replace:

```python
    # def create_vector(self, doc, user_openai_api_key=None):
    #     logger.info("Creating vector for document")
    #     logger.info(f"Document: {doc}")
    #     if user_openai_api_key:
    #         self.commons["documents_vector_store"]._embedding = OpenAIEmbeddings(
    #             openai_api_key=user_openai_api_key
    #         )  # pyright: ignore reportPrivateUsage=none
    #     try:
    #         sids = self.commons["documents_vector_store"].add_documents([doc])
    #         if sids and len(sids) > 0:
    #             return sids

    #     except Exception as e:
    #         logger.error(f"Error creating vector for document {e}")

    def create_vector(self, doc, user_openai_api_key=None):
        logger.info("Creating vector for document")
        logger.info(f"Document: {doc}")
        self.commons["documents_vector_store"]._embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cuda'},
        encode_kwargs={'normalize_embeddings': False}
        )  # pyright: ignore reportPrivateUsage=none
        logger.info('||| creating embedding')
        try:
            sids = self.commons["documents_vector_store"].add_documents([doc])
            if sids and len(sids) > 0:
                return sids

        except Exception as e:
            logger.error(f"Error creating vector for document {e}")
```

<a name="llm"/>

## Local LLM

The final step is to use a local model from HuggingFace for inference. (The HF token is optional, only required for certain models on HF.)

Update the Quivr backend dockerfile:

```
    ENV HUGGINGFACEHUB_API_TOKEN=hf_XXX

    RUN pip install accelerate
```

Update the `private_gpt4all.py` file as follows:

```python
    import langchain
    langchain.debug = True
    langchain.verbose = True

    import os
    import transformers
    from langchain.llms import HuggingFacePipeline
    from langchain.embeddings import HuggingFaceEmbeddings
    ...

    model_id = "stabilityai/StableBeluga-13B"
    ...

    def _create_llm(
        self,
        model,
        streaming=False,
        callbacks=None,
    ) -> BaseLLM:
        """
        Override the _create_llm method to enforce the use of a private model.
        :param model: Language model name to be used.
        :param streaming: Whether to enable streaming of the model
        :param callbacks: Callbacks to be used for streaming
        :return: Language model instance
        """

        model_path = self.model_path

        logger.info("Using private model: %s", model)
        logger.info("Streaming is set to %s", streaming)
        logger.info("--- model  %s",model)

        logger.info("--- model path %s",model_path)

        model_id = "stabilityai/StableBeluga-13B"

        llm = transformers.AutoModelForCausalLM.from_pretrained(
            model_id,
            use_cache=True,
            load_in_4bit=True,
            device_map='auto',
            #use_auth_token=hf_auth
        )
        logger.info('<<< transformers.AutoModelForCausalLM.from_pretrained')

        llm.eval()
        logger.info('<<< eval')

        tokenizer = transformers.AutoTokenizer.from_pretrained(
            model_id,
            use_auth_token=hf_auth
        )
        logger.info('<<< transformers.AutoTokenizer.from_pretrained')

        generate_text = transformers.pipeline(
            model=llm, tokenizer=tokenizer,
            return_full_text=True,  # langchain expects the full text
            task='text-generation',
            # we pass model parameters here too
            #stopping_criteria=stopping_criteria,  # without this model rambles during chat
            temperature=0.5,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
            max_new_tokens=512,  # mex number of tokens to generate in the output
            repetition_penalty=1.1  # without this output begins repeating
        )
        logger.info('<<< generate_text = transformers.pipeline(')

        result = HuggingFacePipeline(pipeline=generate_text)

        logger.info('<<< generate_text = transformers.pipeline(')

        logger.info("<<< created llm HuggingFace")
        return result
```
