from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict


class QuivrBaseConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @classmethod
    def from_yaml(cls, file_path: str | Path):
        # Load the YAML file
        with open(file_path, "r") as stream:
            config_data = yaml.safe_load(stream)

        # Instantiate the class using the YAML data
        return cls(**config_data)
