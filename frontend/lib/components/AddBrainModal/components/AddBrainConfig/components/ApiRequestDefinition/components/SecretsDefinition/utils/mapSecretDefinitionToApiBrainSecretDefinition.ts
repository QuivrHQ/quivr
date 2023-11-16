import { ApiBrainDefinitionSecret } from "@/lib/api/brain/types";

import { SecretDefinition } from "../types";

export type ApiBrainSecretsDefinitionsAndValues = {
  secrets: ApiBrainDefinitionSecret[];
  brain_secrets_values: Record<string, string>;
};

export const mapSecretDefinitionToApiBrainSecretsDefinitionsAndValue = (
  secretDefinitions: SecretDefinition[]
): ApiBrainSecretsDefinitionsAndValues => {
  const secrets: ApiBrainDefinitionSecret[] = secretDefinitions.map(
    (secretDefinition) => {
      const { name, type, description } = secretDefinition;

      return { name, type, description };
    }
  );

  const brain_secrets_values: Record<string, string> = secretDefinitions.reduce(
    (acc, secretDefinition) => {
      const { name, value } = secretDefinition;

      return { ...acc, [name]: value };
    },
    {}
  );

  return { secrets, brain_secrets_values };
};
