import { useEffect } from "react";
import { useForm, useFormContext, useWatch } from "react-hook-form";

import { ApiBrainDefinitionSchema } from "@/lib/api/brain/types";

import { defaultParamDefinitionRow } from "../config";
import { ParameterDefinition } from "../types";
import { mapApiBrainDefinitionSchemaToParameterDefinition } from "../utils/mapApiBrainDefinitionSchemaToParameterDefinition";
import { mapParameterDefinitionToApiBrainDefinitionSchema } from "../utils/mapParameterDefinitionToApiBrainDefinitionSchema";

type UseParamsDefinitionProps = {
  name: string;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useParamsDefinition = ({ name }: UseParamsDefinitionProps) => {
  const { getValues: getContextValues } = useFormContext<{
    [name: string]: ApiBrainDefinitionSchema;
  }>();

  const { setValue } = useFormContext();

  const { control, register } = useForm<{
    [name: string]: ParameterDefinition[];
  }>({
    defaultValues: {
      [name]: [defaultParamDefinitionRow],
    },
  });

  useEffect(() => {
    const existingDefinition = getContextValues(name);

    setValue(
      name,
      mapApiBrainDefinitionSchemaToParameterDefinition(existingDefinition)
    );
  }, [name, getContextValues, setValue]);

  const params = useWatch({
    control,
    name,
  });

  useEffect(() => {
    const paramsWithValues = params.filter(
      (param) => param.name !== "" && param.description !== ""
    );

    setValue(
      name,
      mapParameterDefinitionToApiBrainDefinitionSchema(paramsWithValues)
    );
  }, [params, name, setValue]);

  return {
    control,
    register,
  };
};
