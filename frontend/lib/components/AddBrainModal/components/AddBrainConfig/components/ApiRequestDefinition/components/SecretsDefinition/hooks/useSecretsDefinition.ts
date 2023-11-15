import { useEffect } from "react";
import { useForm, useFormContext, useWatch } from "react-hook-form";

import {
  brainSecretsSchemaDefinitionKeyInForm,
  brainSecretsValueKeyInForm,
  defaultSecretDefinitionRow,
} from "../config";
import { SecretDefinition, SecretRelatedFields } from "../types";
import { mapSecretDefinitionToApiBrainSecretsDefinitionsAndValue } from "../utils/mapSecretDefinitionToApiBrainSecretDefinition";
import { mapSecretsDefinitionsAndValuesToSecretDefinition } from "../utils/mapSecretsDefinitionsAndValuesToSecretDefinition";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSecretsDefinition = () => {
  const { getValues: getContextValues } = useFormContext<{
    [brainSecretsSchemaDefinitionKeyInForm]: SecretDefinition[];
    [brainSecretsValueKeyInForm]: Record<string, string>;
  }>();
  const { setValue } = useFormContext();

  const { register, control } = useForm<SecretRelatedFields>({
    defaultValues: {
      [brainSecretsSchemaDefinitionKeyInForm]: [defaultSecretDefinitionRow],
    },
  });

  useEffect(() => {
    const existingSecretsDefinitionsSchemas = getContextValues(
      brainSecretsSchemaDefinitionKeyInForm
    );
    const existingSecretsValues = getContextValues(brainSecretsValueKeyInForm);

    const secretDefinition = mapSecretsDefinitionsAndValuesToSecretDefinition(
      existingSecretsDefinitionsSchemas,
      existingSecretsValues
    );
    if (secretDefinition.length === 0) {
      return;
    }
    setValue(brainSecretsSchemaDefinitionKeyInForm, secretDefinition);
  }, [getContextValues, setValue]);

  const secretsDefinitionSchemas = useWatch({
    control,
    name: brainSecretsSchemaDefinitionKeyInForm,
  }) as SecretDefinition[] | undefined;

  useEffect(() => {
    if (secretsDefinitionSchemas === undefined) {
      return;
    }
    const paramsWithValues = secretsDefinitionSchemas.filter(
      (param) => param.name !== "" && param.description !== ""
    );

    const { secrets, brain_secrets_values } =
      mapSecretDefinitionToApiBrainSecretsDefinitionsAndValue(paramsWithValues);

    setValue(brainSecretsSchemaDefinitionKeyInForm, secrets);
    setValue(brainSecretsValueKeyInForm, brain_secrets_values);
  }, [secretsDefinitionSchemas, setValue]);

  return {
    control,
    register,
  };
};
