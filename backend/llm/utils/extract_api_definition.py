from models.ApiBrainDefinition import ApiBrainDefinitionSchemaProperty


def format_api_brain_property(property: ApiBrainDefinitionSchemaProperty):
    property_data: dict = {
        "type": property.type,
        "description": property.description,
    }
    if property.enum:
        property_data["enum"] = property.enum
    return property_data
