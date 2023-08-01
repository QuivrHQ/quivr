from models.prompt import Prompt
from models.settings import common_dependencies


def get_public_prompts() -> list[Prompt]:
    """
    List all public prompts
    """
    commons = common_dependencies()

    return (
        commons["supabase"]
        .from_("prompts")
        .select("*")
        .filter("status", "eq", "public")
        .execute()
    ).data
