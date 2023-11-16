import { SecretDefinition } from "./types";

export const defaultSecretDefinitionRow: SecretDefinition = {
  name: "",
  type: "string",
  value: "",
  description: "",
};

export const brainSecretsSchemaDefinitionKeyInForm = "brain_definition.secrets";
export const brainSecretsValueKeyInForm = "brain_secrets_values";
