from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models import FakeListChatModel

from quivr_core import Brain
from quivr_core.config import LLMEndpointConfig
from quivr_core.llm.llm_endpoint import LLMEndpoint

if __name__ == "__main__":
    brain = Brain.from_files(
        name="test_brain",
        file_paths=["tests/processor/data/dummy.pdf"],
        llm=LLMEndpoint(
            llm=FakeListChatModel(responses=["good"]),
            llm_config=LLMEndpointConfig(model="fake_model"),
        ),
        embedder=DeterministicFakeEmbedding(size=20),
    )
    # Check brain info
    print(brain)

    # Ask brain

    while True:
        # Get user input
        question = input("question: ").strip()

        # Check if user wants to exit
        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Generate a random response
        answer = brain.ask(question)

        # Print the answer
        print(f"answer: {answer.answer}")
