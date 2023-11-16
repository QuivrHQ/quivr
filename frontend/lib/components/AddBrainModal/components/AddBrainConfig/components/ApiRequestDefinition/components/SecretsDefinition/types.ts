import { ApiBrainDefinitionSchemaPropertyType } from "@/lib/api/brain/types";

export type SecretDefinition = {
  name: string;
  type: ApiBrainDefinitionSchemaPropertyType;
  description: string;
  value: string;
};

export type SecretRelatedFields = {
  [name: string]: SecretDefinition[];
};
