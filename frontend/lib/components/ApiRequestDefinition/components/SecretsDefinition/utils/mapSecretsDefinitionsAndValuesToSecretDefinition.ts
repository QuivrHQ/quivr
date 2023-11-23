import { ApiBrainDefinitionSecret } from "@/lib/api/brain/types";

import { defaultSecretDefinitionRow } from "../config";
import { SecretDefinition } from "../types";

export const mapSecretsDefinitionsAndValuesToSecretDefinition = (
  apiBrainSecretsDefinitions?: ApiBrainDefinitionSecret[],
  brainSecretsValue?: Record<string, string>
): SecretDefinition[] => {
  if (
    apiBrainSecretsDefinitions === undefined ||
    apiBrainSecretsDefinitions.length === 0
  ) {
    return [defaultSecretDefinitionRow];
  }

  const secretDefinition: SecretDefinition[] = apiBrainSecretsDefinitions.map(
    (secret) => {
      const { name, type, description } = secret;
      const value = brainSecretsValue?.[name] ?? "";

      return { name, type, description, value };
    }
  );

  return secretDefinition;
};
