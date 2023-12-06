import { useFormContext } from "react-hook-form";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainKnowledgeStep = () => {
  const { watch } = useFormContext<CreateBrainProps>();
  const brainType = watch("brain_type");
  const url = watch("brain_definition.url");
  const compositeBrainConnections = watch("connected_brains_ids") ?? [];
  const isApiBrain = brainType === "api";
  const isCompositeBrain = brainType === "composite";

  const isApiBrainDefinitionsFilled = url !== "";

  const isSubmitButtonDisabled =
    (isCompositeBrain && compositeBrainConnections.length === 0) ||
    (isApiBrain && !isApiBrainDefinitionsFilled);

  return {
    brainType,
    isSubmitButtonDisabled,
  };
};
