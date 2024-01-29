from llm.knowledge_brain_qa import generate_source


def test_generate_source_no_documents():
    result = {"source_documents": []}
    brain = {"brain_id": "123"}

    sources = generate_source(result, brain)

    assert sources == []


def test_generate_source_with_url():
    result = {
        "source_documents": [
            {
                "metadata": {
                    "original_file_name": "http://example.com",
                }
            }
        ]
    }
    brain = {"brain_id": "123"}

    sources = generate_source(result, brain)

    assert len(sources) == 1
    assert sources[0].name == "http://example.com"
    assert sources[0].type == "url"
    assert sources[0].source_url == "http://example.com"
    assert sources[0].original_file_name == "http://example.com"
