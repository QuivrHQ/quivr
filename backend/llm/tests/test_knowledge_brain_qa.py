from llm.knowledge_brain_qa import generate_source


def test_generate_source_no_documents():
    result = {"source_documents": []}
    brain = {"brain_id": "123"}

    sources = generate_source(result, brain)

    assert sources == []
