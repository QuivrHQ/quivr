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
    const { openAiKey } = getValues();

    const isKeyEmpty = openAiKey === undefined || openAiKey === "";

    if (isKeyEmpty || openAiKeyPattern.test(openAiKey)) {
      if (isKeyEmpty) {
        localStorage.removeItem("openAiKey");
      } else {
        localStorage.setItem("openAiKey", openAiKey);
      }

      updateConfig({ openAiKey });
      publish({
        text: "Config saved",
        variant: "success",
      });
    } else {
      publish({
        text: "Invalid OpenAI Key",
        variant: "danger",
      });
      setError("openAiKey", { type: "pattern", message: "Invalid OpenAI Key" });
    }
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
