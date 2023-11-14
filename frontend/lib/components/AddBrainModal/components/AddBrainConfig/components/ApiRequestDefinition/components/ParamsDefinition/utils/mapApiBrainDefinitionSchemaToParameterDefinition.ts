import { ApiBrainDefinitionSchema } from "@/lib/api/brain/types";

import { ParameterDefinition } from "../types";

export const mapApiBrainDefinitionSchemaToParameterDefinition = (
  schema?: ApiBrainDefinitionSchema
): ParameterDefinition[] => {
  if (schema === undefined) {
    return [];
  }
  const { properties, required } = schema;

  return properties.map((property) => {
    const { name, type, description } = property;

    return {
      name,
      type: type === "string" ? "string" : "number",
      required: required.includes(name),
      description,
    };
  });
};
