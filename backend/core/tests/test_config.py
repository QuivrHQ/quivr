from quivr_core.config import LLMEndpointConfig, RAGConfig


def test_default_llm_config():
    config = LLMEndpointConfig()

    assert (
        config.model_dump()
        == LLMEndpointConfig(
            model="gpt-3.5-turbo-0125",
            llm_base_url=None,
            llm_api_key=None,
            max_input=2000,
            max_tokens=2000,
            temperature=0.7,
            streaming=True,
        ).model_dump()
    )


def test_default_ragconfig():
    config = RAGConfig()

    assert config.max_files == 20
    assert config.prompt is None
    assert config.llm_config == LLMEndpointConfig()
