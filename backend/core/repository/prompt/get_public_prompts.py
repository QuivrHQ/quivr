from models.prompt import Prompt
from models.settings import common_dependencies


def get_public_prompts() -> list[Prompt]:
    """
    List all public prompts
    """
    commons = common_dependencies()
    return commons["db"].get_public_prompts()
