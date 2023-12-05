import { ApiBrainDefinitionSchemaPropertyType } from "@/lib/api/brain/types";

import { brainSecretsSchemaDefinitionKeyInForm } from "./config";

export type SecretDefinition = {
  name: string;
  type: ApiBrainDefinitionSchemaPropertyType;
  description: string;
  value: string;
};

export type SecretRelatedFields = {
  [brainSecretsSchemaDefinitionKeyInForm]: SecretDefinition[];
};
