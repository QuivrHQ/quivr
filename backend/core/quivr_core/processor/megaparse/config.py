from enum import Enum

import yaml
from pydantic import BaseModel


class PdfParser(str, Enum):
    LLAMA_PARSE = "llama_parse"
    UNSTRUCTURED = "unstructured"
    MEGAPARSE_VISION = "megaparse_vision"


class MegaparseBaseConfig(BaseModel):
    @classmethod
    def from_yaml(cls, file_path: str):
        # Load the YAML file
        with open(file_path, "r") as stream:
            config_data = yaml.safe_load(stream)

        # Instantiate the class using the YAML data
        return cls(**config_data)


class MegaparseConfig(MegaparseBaseConfig):
    strategy: str = "fast"
    llama_parse_api_key: str | None = None
    pdf_parser: PdfParser = PdfParser.UNSTRUCTURED
