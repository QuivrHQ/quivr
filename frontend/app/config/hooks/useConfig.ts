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
    setError,
  } = useForm({
    defaultValues: config,
  });

  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");

  useEffect(() => {
    reset(config);
  }, [config, reset]);

  const openAiKeyPattern = /^sk-[a-zA-Z0-9]{45,50}$/;

  const saveConfig = () => {
    const values = getValues();

    if (values.openAiKey != null && !openAiKeyPattern.test(values.openAiKey)) {
      publish({
        text: "Invalid OpenAI Key",
        variant: "danger",
      });
      setError("openAiKey", { type: "pattern", message: "Invalid OpenAI Key" });
      return;
    } else {
      localStorage.setItem("openAiKey", values.openAiKey ?? "");
    }

    updateConfig(values);
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
