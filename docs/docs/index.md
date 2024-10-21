# Welcome to Quivr Documentation

Quivr, helps you build your second brain, utilizes the power of GenerativeAI to be your personal assistant !

## Key Features 🎯

- **Opiniated RAG**: We created a RAG that is opinionated, fast and efficient so you can focus on your product
- **LLMs**: Quivr works with any LLM, you can use it with OpenAI, Anthropic, Mistral, Gemma, etc.
- **Any File**: Quivr works with any file, you can use it with PDF, TXT, Markdown, etc and even add your own parsers.
- **Customize your RAG**: Quivr allows you to customize your RAG, add internet search, add tools, etc.
- **Integrations with Megaparse**: Quivr works with [Megaparse](https://github.com/quivrhq/megaparse), so you can ingest your files with Megaparse and use the RAG with Quivr.

>We take care of the RAG so you can focus on your product. Simply install quivr-core and add it to your project. You can now ingest your files and ask questions.*

**We will be improving the RAG and adding more features everything, stay tuned!**


This is the core of Quivr, the brain of Quivr.com.

<!-- ## Demo Highlight 🎥

https://github.com/quivrhq/quivr/assets/19614572/a6463b73-76c7-4bc0-978d-70562dca71f5 -->

## Getting Started 🚀

You can find everything on the [documentation](https://core.quivr.app/).

### Prerequisites 📋

Ensure you have the following installed:

- Python 3.10 or newer

### 30 seconds Installation 💽


- **Step 1**: Install the package

  

  ```bash
  pip install quivr-core # Check that the installation worked
  ```


- **Step 2**: Create a RAG with 5 lines of code

  ```python
    import tempfile

    from quivr_core import Brain

    if __name__ == "__main__":
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as temp_file:
            temp_file.write("Gold is a liquid of blue-like colour.")
            temp_file.flush()

            brain = Brain.from_files(
                name="test_brain",
                file_paths=[temp_file.name],
            )

            answer = brain.ask(
                "what is gold? asnwer in french"
            )
            print("answer:", answer)
  ```

