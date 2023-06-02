import { useToast } from "@/lib/hooks/useToast";
import { useForm } from "react-hook-form";

import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useEffect } from "react";

export const useConfig = () => {
  const { config, updateConfig, resetConfig } = useBrainConfig();
  const { publish } = useToast();
  const {
    register,
    handleSubmit,
    watch,
    getValues,
    reset,
    formState: { isDirty },
  } = useForm({
    defaultValues: config,
  });

  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

  useEffect(() => {
    reset(config);
  }, [config, reset]);

  const saveConfig = () => {
    updateConfig(getValues());
    publish({
      text: "Config saved",
      variant: "success",
    });
  };

  const resetBrainConfig = () => {
    resetConfig();
    publish({
      text: "Config reset",
      variant: "success",
    });
  };

  return {
    handleSubmit,
    saveConfig,
    maxTokens,
    temperature,
    isDirty,
    register,
    model,
    resetBrainConfig,
  };
};
