from quivr_core.base_config import QuivrBaseConfig
from quivr_core.rag.prompts import TemplatePromptName


class PromptConfig(QuivrBaseConfig):
    prompt: str | None = None
    template_name: TemplatePromptName | None = None
