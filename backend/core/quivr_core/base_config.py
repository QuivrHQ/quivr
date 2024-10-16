from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict
from typing import Self


class QuivrBaseConfig(BaseModel):
    """
    Base configuration class for Quivr.

    This class extends Pydantic's BaseModel and provides a foundation for
    configuration management in quivr-core.

    Attributes:
        model_config (ConfigDict): Configuration for the Pydantic model.
            It's set to forbid extra attributes, ensuring strict adherence
            to the defined schema.

    Class Methods:
        from_yaml: Create an instance of the class from a YAML file.
    """

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def from_yaml(cls, file_path: str | Path) -> Self:
        """
        Create an instance of the class from a YAML file.

        Args:
            file_path (str | Path): The path to the YAML file.

        Returns:
            QuivrBaseConfig: An instance of the class initialized with the data from the YAML file.
        """
        # Load the YAML file
        with open(file_path, "r") as stream:
            config_data = yaml.safe_load(stream)

        # Instantiate the class using the YAML data
        return cls(**config_data)
