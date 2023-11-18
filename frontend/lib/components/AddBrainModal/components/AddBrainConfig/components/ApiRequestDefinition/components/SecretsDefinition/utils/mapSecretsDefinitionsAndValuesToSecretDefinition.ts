import { ApiBrainDefinition } from "@/lib/api/brain/types";

import { defaultSecretDefinitionRow } from "../config";
import { SecretDefinition } from "../types";

export const mapSecretsDefinitionsAndValuesToSecretDefinition = (
  apiBrainDefinition?: ApiBrainDefinition,
  brainSecretsValue?: Record<string, string>
): SecretDefinition[] => {
  if (
    apiBrainDefinition === undefined ||
    brainSecretsValue === undefined ||
    apiBrainDefinition.secrets === undefined ||
    apiBrainDefinition.secrets.length === 0
  ) {
    return [defaultSecretDefinitionRow];
  }

  const secrets = apiBrainDefinition.secrets;

  const secretDefinition: SecretDefinition[] = secrets.map((secret) => {
    const { name, type } = secret;
    const value = brainSecretsValue[name] ?? "";

    return { name, type, description: "", value };
  });

  return secretDefinition;
};
