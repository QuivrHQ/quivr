from models.brain_entity import BrainEntity
from repository.api_brain_definition.get_api_brain_definition import (
    get_api_brain_definition,
)


def get_api_brain_definition_as_json_schema(brain: BrainEntity):
    if not brain:
        raise Exception("No brain found")

    api_brain_definition = get_api_brain_definition(brain.id)
    if not api_brain_definition:
        raise Exception("No api brain definition found")

    required = []
    required.extend(api_brain_definition.params.required)
    required.extend(api_brain_definition.search_params.required)

    properties = {}
    for property in api_brain_definition.params.properties:
        properties[property.name] = property
    for property in api_brain_definition.search_params.properties:
        properties[property.name] = property

    parameters = {
        "type": "object",
        "properties": properties,
        "required": required,
    }
    schema = {
        "name": brain.name,
        "description": brain.description,
        "parameters": parameters,
    }

    return schema
