from fastapi import HTTPException
from llm.utils.extract_api_definition import (
    format_api_brain_property,
)
from llm.utils.sanitize_function_name import sanitize_function_name
from models.brain_entity import BrainEntity
from repository.api_brain_definition.get_api_brain_definition import (
    get_api_brain_definition,
)


def get_api_brain_definition_as_json_schema(brain: BrainEntity):
    api_brain_definition = get_api_brain_definition(brain.id)
    if not api_brain_definition:
        raise HTTPException(
            status_code=404, detail=f"Brain definition {brain.id} not found"
        )

    required = []
    required.extend(api_brain_definition.params.required)
    required.extend(api_brain_definition.search_params.required)
    properties = {}

    api_properties = (
        api_brain_definition.params.properties
        + api_brain_definition.search_params.properties
    )

    for property in api_properties:
        properties[property.name] = format_api_brain_property(property)

    parameters = {
        "type": "object",
        "properties": properties,
        "required": required,
    }
    schema = {
        "name": sanitize_function_name(brain.name),
        "description": brain.description,
        "parameters": parameters,
    }

    return schema
