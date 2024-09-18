import tempfile

from quivr_core import Brain
from quivr_core.quivr_rag import QuivrQARAG
from quivr_core.quivr_rag_langgraph import QuivrQARAGLangGraph

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as temp_file:
        temp_file.write("Gold is a liquid of blue-like colour.")
        temp_file.flush()

        brain = Brain.from_files(
            name="test_brain",
            file_paths=[temp_file.name],
        )

        answer = brain.ask(
            "what is gold? asnwer in french", rag_pipeline=QuivrQARAGLangGraph
        )
        print("answer QuivrQARAGLangGraph :", answer.answer)

        answer = brain.ask("what is gold? asnwer in french", rag_pipeline=QuivrQARAG)
        print("answer QuivrQARAG :", answer.answer)
