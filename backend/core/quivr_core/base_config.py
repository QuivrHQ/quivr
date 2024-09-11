from pydantic import BaseModel
import yaml


class QuivrBaseConfig(BaseModel):
    @classmethod
    def from_yaml(cls, file_path: str):
        # Load the YAML file
        with open(file_path, 'r') as stream:
            config_data = yaml.safe_load(stream)
        
        # Instantiate the class using the YAML data
        return cls(**config_data)