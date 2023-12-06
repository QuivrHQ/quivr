import { useFormContext } from "react-hook-form";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainKnowledgeStep = () => {
  const { watch } = useFormContext<CreateBrainProps>();
  const brainType = watch("brain_type");
  const url = watch("brain_definition.url");
  const isApiBrain = brainType === "api";
  const isChatflowBrain = brainType === "chatflow";

  const isApiBrainDefinitionsFilled = url !== "";

  const isSubmitButtonDisabled =
    isChatflowBrain || (isApiBrain && !isApiBrainDefinitionsFilled);

  return {
    brainType,
    isSubmitButtonDisabled,
  };
};
