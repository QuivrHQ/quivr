import {
  ApiBrainDefinitionSchema,
  ApiBrainDefinitionSchemaProperty,
} from "@/lib/api/brain/types";

import { ParameterDefinition } from "../types";

export const mapParameterDefinitionToApiBrainDefinitionSchema = (
  params: ParameterDefinition[]
): ApiBrainDefinitionSchema => {
  const properties: ApiBrainDefinitionSchemaProperty[] = [];
  const required: string[] = [];

  params.forEach((param) => {
    const { name, type, required: isRequired, description } = param;

    const property: ApiBrainDefinitionSchemaProperty = {
      name,
      type: type === "string" ? "string" : "number",
      description,
    };

    properties.push(property);

    if (isRequired) {
      required.push(name);
    }
  });

  return {
    properties,
    required,
  };
};
