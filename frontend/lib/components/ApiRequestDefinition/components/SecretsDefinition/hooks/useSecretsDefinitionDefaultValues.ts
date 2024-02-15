import { useFormContext } from "react-hook-form";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types/types";

import {
  brainSecretsValueKeyInForm,
  defaultSecretDefinitionRow,
} from "../config";
import { mapSecretsDefinitionsAndValuesToSecretDefinition } from "../utils/mapSecretsDefinitionsAndValuesToSecretDefinition";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSecretsDefinitionDefaultValues = () => {
  const { getValues: getContextValues } = useFormContext<CreateBrainProps>();

  const existingSecretsDefinitionsSchemas = getContextValues();
  const existingSecretsValues = getContextValues(brainSecretsValueKeyInForm);

  const secretDefinition = mapSecretsDefinitionsAndValuesToSecretDefinition(
    existingSecretsDefinitionsSchemas["brain_definition"]?.secrets,
    existingSecretsValues
  );

  const defaultValues =
    secretDefinition.length > 0
      ? secretDefinition
      : [defaultSecretDefinitionRow];

  return {
    defaultValues,
  };
};
