# Configuration

The configuration classes are based on [Pydantic](https://docs.pydantic.dev/latest/) and allow the configuration of the ingestion and retrieval workflows via YAML files.

Below is an example of a YAML configuration file for a basic RAG retrieval workflow.
```yaml
workflow_config:
  name: "standard RAG"
  nodes:
    - name: "START"
      edges: ["filter_history"]

    - name: "filter_history"
      edges: ["rewrite"]

    - name: "rewrite"
      edges: ["retrieve"]

    - name: "retrieve"
      edges: ["generate_rag"]

    - name: "generate_rag" # the name of the last node, from which we want to stream the answer to the user, should always start with "generate"
      edges: ["END"]
# Maximum number of previous conversation iterations
# to include in the context of the answer
max_history: 10

prompt: "my prompt"

max_files: 20
reranker_config:
  # The reranker supplier to use
  supplier: "cohere"

  # The model to use for the reranker for the given supplier
  model: "rerank-multilingual-v3.0"

  # Number of chunks returned by the reranker
  top_n: 5
llm_config:

  max_context_tokens: 2000

  temperature: 0.7
  streaming: true
```
