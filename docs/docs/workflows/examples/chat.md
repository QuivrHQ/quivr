# Chat

Creating a custom brain workflow is simple, here are the steps : 

1. Create a workflow
2. Create a Brain with this workflow and append your files
3. Launch a chat
4. Chat with your brain ! 

### Use AssistantConfig

First create a json configuration file in the rag_config_workflow.yaml format (see workflows):
```yaml
ingestion_config:
  parser_config:
    megaparse_config:
      strategy: "fast"
      pdf_parser: "unstructured"
    splitter_config:
      chunk_size: 400
      chunk_overlap: 100

retrieval_config:
  workflow_config:
    name: "standard RAG"
    nodes:
      - name: "START"
        edges: ["filter_history"]

      - name: "filter_history"
        edges: ["generate_chat_llm"]

      - name: "generate_chat_llm" # the name of the last node, from which we want to stream the answer to the user, should always start with "generate"
        edges: ["END"]
  # Maximum number of previous conversation iterations
  # to include in the context of the answer
  max_history: 10

  #prompt: "my prompt"

  max_files: 20
  reranker_config:
    # The reranker supplier to use
    supplier: "cohere"

    # The model to use for the reranker for the given supplier
    model: "rerank-multilingual-v3.0"

    # Number of chunks returned by the reranker
    top_n: 5
  llm_config:
    # The LLM supplier to use
    supplier: "openai"

    # The model to use for the LLM for the given supplier
    model: "gpt-3.5-turbo-0125"

    max_input_tokens: 2000

    # Maximum number of tokens to pass to the LLM
    # as a context to generate the answer
    max_output_tokens: 2000

    temperature: 0.7
    streaming: true

```
This brain is set up to : 
    * Filter history and keep only the latest conversations
    * Ask the question to the brain
    * Generate answer

    
Then, when instanciating your Brain, add the custom config you created: 

```python
    assistant_config = AssistantConfig.from_yaml("my_config_file.yaml")
    processor_kwargs = {
        "assistant_config": assistant_config
    }

```






