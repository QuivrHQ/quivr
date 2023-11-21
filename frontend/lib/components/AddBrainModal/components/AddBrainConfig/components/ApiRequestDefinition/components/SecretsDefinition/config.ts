import { SecretDefinition } from "./types";

export const defaultSecretDefinitionRow: SecretDefinition = {
  name: "",
  type: "string",
  value: "",
  description: "",
};

export const brainSecretsSchemaDefinitionKeyInForm = "secrets";
export const brainSecretsValueKeyInForm = "brain_secrets_values";
