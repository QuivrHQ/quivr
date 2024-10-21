from quivr_core.config import LLMEndpointConfig, RetrievalConfig


def test_default_llm_config():
    config = LLMEndpointConfig()

    assert config.model_dump(exclude={"llm_api_key"}) == LLMEndpointConfig(
        model="gpt-4o",
        llm_base_url=None,
        llm_api_key=None,
        max_input_tokens=2000,
        max_output_tokens=2000,
        temperature=0.7,
        streaming=True,
    ).model_dump(exclude={"llm_api_key"})


def test_default_retrievalconfig():
    config = RetrievalConfig()

    assert config.max_files == 20
    assert config.prompt is None
    assert config.llm_config.model_dump(
        exclude={"llm_api_key"}
    ) == LLMEndpointConfig().model_dump(exclude={"llm_api_key"})
