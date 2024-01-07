import { useFormContext } from "react-hook-form";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types";

import { defaultParamDefinitionRow } from "../config";
import { mapApiBrainDefinitionSchemaToParameterDefinition } from "../utils/mapApiBrainDefinitionSchemaToParameterDefinition";

type UseParamsDefinitionDefaultValuesProps = {
  dataKey: "brain_definition.params" | "brain_definition.search_params";
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useParamsDefinitionDefaultValues = ({
  dataKey,
}: UseParamsDefinitionDefaultValuesProps) => {
  const { getValues: getContextValues } = useFormContext<CreateBrainProps>();

  const existingDefinition = getContextValues(dataKey);

  const paramsDefinition =
    mapApiBrainDefinitionSchemaToParameterDefinition(existingDefinition);

  const defaultValues =
    paramsDefinition.length > 0
      ? paramsDefinition
      : [defaultParamDefinitionRow];

  return {
    defaultValues,
  };
};
