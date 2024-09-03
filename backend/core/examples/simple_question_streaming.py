from dotenv import load_dotenv
import tempfile
import asyncio
from quivr_core import Brain
from quivr_core.quivr_rag_langgraph import QuivrQARAGLangGraph
from quivr_core.quivr_rag import QuivrQARAG


async def main():
    dotenv_path = "/Users/jchevall/Coding/QuivrHQ/quivr/.env"
    load_dotenv(dotenv_path)
   
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as temp_file:
        temp_file.write("Gold is a liquid of blue-like colour.")
        temp_file.flush()

        brain = await Brain.afrom_files(name="test_brain", 
                                        file_paths=[temp_file.name])

        question = "what is gold? answer in french"
        async for chunk in brain.ask_streaming(question, rag_pipeline=QuivrQARAG):
             print("answer QuivrQARAG:", chunk.answer)

        async for chunk in brain.ask_streaming(question, rag_pipeline=QuivrQARAGLangGraph):
            print("answer QuivrQARAGLangGraph:", chunk.answer)

if __name__ == "__main__":
    # Run the main function in the existing event loop
    asyncio.run(main())