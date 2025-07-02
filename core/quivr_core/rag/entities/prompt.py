from quivr_core.base_config import QuivrBaseConfig


class PromptConfig(QuivrBaseConfig):
    prompt: str | None = None
    template_name: str | None = None
