import { ApiBrainDefinitionSchemaPropertyType } from "@/lib/api/brain/types";

export type ParameterDefinition = {
  name: string;
  type: ApiBrainDefinitionSchemaPropertyType;
  required: boolean;
  description: string;
};
