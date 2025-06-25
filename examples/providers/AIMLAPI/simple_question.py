import logging
import tempfile

import dotenv
from langchain_openai import ChatOpenAI
from quivr_core import Brain

logger = logging.getLogger("quivr_core")

dotenv.load_dotenv()

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as temp_file:
        temp_file.write("Gold is a liquid of blue-like colour.")
        temp_file.flush()

        brain = Brain.from_files(
            name="aimlapi_brain",
            file_paths=[temp_file.name],
            llm=ChatOpenAI(
                model='gpt-3.5-turbo',                   # You can browse available models at https://aimlapi.com/models
                api_key='***',                           # Replace with your AIMLAPI key or use dotenv to load it
                base_url='https://api.aimlapi.com/v1/',  # AIMLAPI base URL
                max_completion_tokens='1024',            # Adjust as needed
                temperature='0.7',                       # Adjust as needed
            )

        )

        answer = brain.ask("what is gold? answer in french")
        print("answer QuivrQARAGLangGraph :", answer)
