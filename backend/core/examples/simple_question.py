import tempfile

from quivr_core import Brain

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as temp_file:
        temp_file.write("Gold is metal.")
        temp_file.flush()

        brain = Brain.from_files(name="test_brain", file_paths=[temp_file.name])

        answer = brain.ask("Property of gold?")

        print("answer :", answer.answer)

        print("brain information: ", brain)
