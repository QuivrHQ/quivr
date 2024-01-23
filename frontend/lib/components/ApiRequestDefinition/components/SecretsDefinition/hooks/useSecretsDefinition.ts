import { useEffect } from "react";
import { useForm, useFormContext, useWatch } from "react-hook-form";

import { useSecretsDefinitionDefaultValues } from "./useSecretsDefinitionDefaultValues";

import { ApiDefinitionContextType } from "../../../types";
import {
  brainSecretsSchemaDefinitionKeyInForm,
  brainSecretsValueKeyInForm,
} from "../config";
import { SecretDefinition } from "../types";
import { mapSecretDefinitionToApiBrainSecretsDefinitionsAndValue } from "../utils/mapSecretDefinitionToApiBrainSecretDefinition";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSecretsDefinition = () => {
  const { setValue: setContextValue, watch: watchContextValue } =
    useFormContext<ApiDefinitionContextType>();
  const { defaultValues } = useSecretsDefinitionDefaultValues();

  const { register, control } = useForm<{
    [brainSecretsSchemaDefinitionKeyInForm]: SecretDefinition[];
  }>({
    defaultValues: {
      [brainSecretsSchemaDefinitionKeyInForm]: defaultValues,
    },
  });

  const secretsDefinitionSchemas = useWatch({
    control,
    name: brainSecretsSchemaDefinitionKeyInForm,
  }) as SecretDefinition[] | undefined;

  const isApiDefinitionReadOnly =
    watchContextValue("isApiDefinitionReadOnly") ?? false;
  const isUpdatingApiDefinition =
    watchContextValue("isUpdatingApiDefinition") ?? false;

  useEffect(() => {
    if (secretsDefinitionSchemas === undefined) {
      return;
    }
    const paramsWithValues = secretsDefinitionSchemas.filter(
      (param) => param.name !== "" && param.description !== ""
    );

    if (paramsWithValues.length === 0) {
      return;
    }

    const { secrets, brain_secrets_values } =
      mapSecretDefinitionToApiBrainSecretsDefinitionsAndValue(paramsWithValues);

    setContextValue("brain_definition.secrets", secrets);
    setContextValue(brainSecretsValueKeyInForm, brain_secrets_values);
  }, [secretsDefinitionSchemas, setContextValue]);

  return {
    control,
    register,
    isApiDefinitionReadOnly,
    isUpdatingApiDefinition,
  };
};
