from typing import Type

from backend.logger import get_logger
from backend.modules.brain.entity.integration_brain import IntegrationEntity
from backend.modules.brain.integrations.Big.Brain import BigBrain
from backend.modules.brain.integrations.GPT4.Brain import GPT4Brain
from backend.modules.brain.integrations.Multi_Contract.Brain import MultiContractBrain
from backend.modules.brain.integrations.Notion.Brain import NotionBrain
from backend.modules.brain.integrations.Proxy.Brain import ProxyBrain
from backend.modules.brain.integrations.Self.Brain import SelfBrain
from backend.modules.brain.integrations.SQL.Brain import SQLBrain
from backend.modules.brain.knowledge_brain_qa import KnowledgeBrainQA

logger = get_logger(__name__)


class RAGServiceFactory:
    integration_list: dict[str, Type[KnowledgeBrainQA]] = {
        "notion": NotionBrain,
        "gpt4": GPT4Brain,
        "sql": SQLBrain,
        "big": BigBrain,
        "doc": KnowledgeBrainQA,
        "proxy": ProxyBrain,
        "self": SelfBrain,
        "multi-contract": MultiContractBrain,
    }

    def get_brain_cls(self, integration: IntegrationEntity):
        pass
