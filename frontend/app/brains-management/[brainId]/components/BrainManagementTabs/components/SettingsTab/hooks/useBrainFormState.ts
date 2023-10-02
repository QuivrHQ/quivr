import { UUID } from "crypto";
import { useForm } from "react-hook-form";

import { defaultBrainConfig } from "@/lib/config/defaultBrainConfig";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { BrainConfig } from "@/lib/types/brainConfig";

import { useBrainFetcher } from "../../../hooks/useBrainFetcher";

type UseBrainFormStateProps = {
  brainId: UUID;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainFormState = ({ brainId }: UseBrainFormStateProps) => {
  const { defaultBrainId } = useBrainContext();

  const {
    register,
    getValues,
    watch,
    setValue,
    reset,
    resetField,
    formState: { dirtyFields },
  } = useForm<BrainConfig>({
    defaultValues: { ...defaultBrainConfig, status: undefined },
  });
  const { brain } = useBrainFetcher({
    brainId,
  });

  const isDefaultBrain = defaultBrainId === brainId;
  const promptId = watch("prompt_id");
  const openAiKey = watch("openAiKey");
  const model = watch("model");
  const temperature = watch("temperature");
  const maxTokens = watch("maxTokens");
  const status = watch("status");

  return {
    brain,
    model,
    temperature,
    maxTokens,
    isDefaultBrain,
    promptId,
    openAiKey,
    dirtyFields,
    status,
    register,
    getValues,
    setValue,
    reset,
    resetField,
  };
};
