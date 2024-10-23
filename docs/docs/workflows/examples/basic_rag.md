# Basic RAG

![](basic_rag.excalidraw.png)


Creating a basic RAG workflow like the one above is simple, here are the steps:


1. Add your API Keys to your environment variables
```python
import os
os.environ["OPENAI_API_KEY"] = "myopenai_apikey"

```
Check our `.env.example` file to see the possible environment variables you can configure. Quivr supports APIs from Anthropic, OpenAI, and Mistral. It also supports local models using Ollama.

2. Create the YAML file ``basic_rag_workflow.yaml`` and copy the following content in it
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

    - name: "generate_rag" # the name of the last node, from which we want to stream the answer to the user
      edges: ["END"]

# Maximum number of previous conversation iterations
# to include in the context of the answer
max_history: 10

# Reranker configuration
reranker_config:
  # The reranker supplier to use
  supplier: "cohere"

  # The model to use for the reranker for the given supplier
  model: "rerank-multilingual-v3.0"

  # Number of chunks returned by the reranker
  top_n: 5

# Configuration for the LLM
llm_config:

  # maximum number of tokens passed to the LLM to generate the answer
  max_input_tokens: 4000

  # temperature for the LLM
  temperature: 0.7
```

3. Create a Brain with the default configuration
```python
from quivr_core import Brain

brain = Brain.from_files(name = "my smart brain",
                        file_paths = ["./my_first_doc.pdf", "./my_second_doc.txt"],
                        )

```

4. Launch a Chat
```python
brain.print_info()

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from quivr_core.config import RetrievalConfig

config_file_name = "./basic_rag_workflow.yaml"

retrieval_config = RetrievalConfig.from_yaml(config_file_name)

console = Console()
console.print(Panel.fit("Ask your brain !", style="bold magenta"))

while True:
    # Get user input
    question = Prompt.ask("[bold cyan]Question[/bold cyan]")

    # Check if user wants to exit
    if question.lower() == "exit":
        console.print(Panel("Goodbye!", style="bold yellow"))
        break

    answer = brain.ask(question, retrieval_config=retrieval_config)
    # Print the answer with typing effect
    console.print(f"[bold green]Quivr Assistant[/bold green]: {answer.answer}")

    console.print("-" * console.width)

brain.print_info()
```

5. You are now all set up to talk with your brain and test different retrieval strategies by simply changing the configuration file!
