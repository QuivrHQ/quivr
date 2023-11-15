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
  const { watch, register } = useFormContext();
  const existingParams = watch(name) as ApiBrainDefinitionSchema;
  const existingProperties =
    mapApiBrainDefinitionSchemaToParameterDefinition(existingParams);

  const { control } = useForm<{
    [name: string]: ParameterDefinition[];
  }>({
    defaultValues: {
      [name]:
        existingProperties.length > 0
          ? existingProperties
          : [defaultParamDefinitionRow],
    },
  });

  const params = useWatch({
    control,
    name,
  });

  const { setValue } = useFormContext();

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
