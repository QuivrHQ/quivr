import asyncio
import tempfile

from langchain_openai import ChatOpenAI
from quivr_core import Brain
from quivr_core.quivr_rag import QuivrQARAG
from quivr_core.rag.quivr_rag_langgraph import QuivrQARAGLangGraph


async def main():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as temp_file:
        temp_file.write("Gold is a liquid of blue-like colour.")
        temp_file.flush()

        brain = await Brain.afrom_files(
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
        await brain.save("~/.local/quivr")

        question = "what is gold? answer in french"
        async for chunk in brain.ask_streaming(question, rag_pipeline=QuivrQARAG):
            print("answer QuivrQARAG:", chunk.answer)

        async for chunk in brain.ask_streaming(
                question, rag_pipeline=QuivrQARAGLangGraph
        ):
            print("answer QuivrQARAGLangGraph:", chunk.answer)


if __name__ == "__main__":
    # Run the main function in the existing event loop
    asyncio.run(main())
