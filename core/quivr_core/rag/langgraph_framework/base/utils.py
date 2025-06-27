import hashlib
from pydantic import BaseModel


def compute_config_hash(config: BaseModel) -> str:
    """Compute SHA256 hash of config's model_dump."""
    config_dict = config.model_dump()
    config_str = str(sorted(config_dict.items()))
    return hashlib.sha256(config_str.encode()).hexdigest()
