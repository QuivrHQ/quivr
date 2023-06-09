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
  const openAiKey = watch("openAiKey");

  useEffect(() => {
    reset(config);
  }, [config, reset]);

  const saveConfig = () => {
    const values = getValues();

    if (!validateConfig()) {
      return;
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

  const openAiKeyPattern = /^sk-[a-zA-Z0-9]{45,50}$/;

  const validateConfig = (): boolean => {
    const { openAiKey } = getValues();

    const isKeyEmpty = openAiKey === "" || openAiKey === undefined;
    if (isKeyEmpty || openAiKeyPattern.test(openAiKey)) {
      return true;
    }

    publish({
      text: "Invalid OpenAI Key",
      variant: "danger",
    });
    setError("openAiKey", { type: "pattern", message: "Invalid OpenAI Key" });

    return false;
  };

  return {
    handleSubmit,
    saveConfig,
    maxTokens,
    openAiKey,
    temperature,
    isDirty,
    register,
    model,
    resetBrainConfig,
  };
};
