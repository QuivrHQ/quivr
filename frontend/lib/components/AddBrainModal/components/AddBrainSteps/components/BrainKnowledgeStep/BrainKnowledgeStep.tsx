import { ApiRequestDefinition } from "@/lib/components/ApiRequestDefinition";
import { BrainType } from "@/lib/types/BrainConfig";

import { CompositeBrainConnections } from "./components/CompositeBrainConnections/CompositeBrainConnections";
import { KnowledgeToFeedInput } from "./components/KnowledgeToFeedInput";
import { useBrainKnowledgeStep } from "./hooks/useBrainKnowledgeStep";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainKnowledgeStep = (): JSX.Element => {
  const { brainType } = useBrainKnowledgeStep();
  const { currentStepIndex } = useBrainCreationSteps();

  const brainTypeToKnowledgeComponent: Record<BrainType, JSX.Element> = {
    doc: <KnowledgeToFeedInput />,
    api: <ApiRequestDefinition />,
    composite: <CompositeBrainConnections />,
  };

  if (currentStepIndex !== 2 || !brainType) {
    return <></>;
  }

  return <>{brainTypeToKnowledgeComponent[brainType]}</>;
};
