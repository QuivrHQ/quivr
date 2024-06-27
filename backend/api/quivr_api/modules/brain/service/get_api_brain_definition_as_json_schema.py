import re

from fastapi import HTTPException
from quivr_api.modules.brain.entity.api_brain_definition_entity import (
    ApiBrainDefinitionSchemaProperty,
)
from quivr_api.modules.brain.entity.brain_entity import BrainEntity
from quivr_api.modules.brain.service.api_brain_definition_service import (
    ApiBrainDefinitionService,
)

api_brain_definition_service = ApiBrainDefinitionService()


def sanitize_function_name(string):
    sanitized_string = re.sub(r"[^a-zA-Z0-9_-]", "", string)

    return sanitized_string


def format_api_brain_property(property: ApiBrainDefinitionSchemaProperty):
    property_data: dict = {
        "type": property.type,
        "description": property.description,
    }
    if property.enum:
        property_data["enum"] = property.enum
    return property_data


def get_api_brain_definition_as_json_schema(brain: BrainEntity):
    api_brain_definition = api_brain_definition_service.get_api_brain_definition(
        brain.id
    )
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
