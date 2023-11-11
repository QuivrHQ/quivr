from fastapi import HTTPException
from models.ApiBrainDefinition import ApiBrainDefinitionSchema


def extract_api_brain_definition_values_from_llm_output(
    brain_schema: ApiBrainDefinitionSchema, arguments: dict
) -> dict:
    params_values = {}
    properties = brain_schema.properties
    required_values = brain_schema.required
    for property in properties:
        if property.name in arguments:
            if property.type == "number":
                params_values[property.name] = float(arguments[property.name])
            else:
                params_values[property.name] = arguments[property.name]
            continue

        if property.name in required_values:
            raise HTTPException(
                status_code=400,
                detail=f"Required parameter {property.name} not found in arguments",
            )

    return params_values
