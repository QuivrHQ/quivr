from models.ApiBrainDefinition import ApiBrainDefinitionSchemaProperty


def extract_brain_api_params_values_from_llm_output(
    params: list[ApiBrainDefinitionSchemaProperty], arguments: dict
):
    params_values = {}

    for param in params:
        if param.name in arguments:
            params_values[param.name] = arguments[param.name]
            continue

        if param.required:
            raise Exception(f"Missing param {param.name}")

    return params_values
