import { useEffect } from "react";
import { useForm, useFormContext, useWatch } from "react-hook-form";

import { useParamsDefinitionDefaultValues } from "./useParamsDefinitionDefaultValues";

import { ApiDefinitionContextType } from "../../../types";
import { ParameterDefinition } from "../types";
import { mapParameterDefinitionToApiBrainDefinitionSchema } from "../utils/mapParameterDefinitionToApiBrainDefinitionSchema";

type UseParamsDefinitionProps = {
  name: "search_params" | "params";
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useParamsDefinition = ({ name }: UseParamsDefinitionProps) => {
  const dataKey = `brain_definition.${name}` as const;

  const { setValue: setContextValue, watch: watchContextValue } =
    useFormContext<ApiDefinitionContextType>();

  const { defaultValues } = useParamsDefinitionDefaultValues({
    dataKey,
  });

  const { control, register } = useForm<{
    [name: string]: ParameterDefinition[];
  }>({
    defaultValues: {
      [name]: defaultValues,
    },
  });

  const isApiDefinitionReadOnly =
    watchContextValue("isApiDefinitionReadOnly") ?? false;

  const params = useWatch({
    control,
    name,
  });

  useEffect(() => {
    const paramsWithValues = params.filter(
      (param) => param.name !== "" && param.description !== ""
    );

    setContextValue(
      dataKey,
      mapParameterDefinitionToApiBrainDefinitionSchema(paramsWithValues)
    );
  }, [params, name, setContextValue, dataKey]);

  return {
    control,
    register,
    isApiDefinitionReadOnly,
  };
};
