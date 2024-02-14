import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { ApiRequestDefinition } from "@/lib/components/ApiRequestDefinition";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { BrainType } from "@/lib/types/BrainConfig";

import styles from "./BrainKnowledgeStep.module.scss";
import { CompositeBrainConnections } from "./components/CompositeBrainConnections/CompositeBrainConnections";
import { useBrainKnowledgeStep } from "./hooks/useBrainKnowledgeStep";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainKnowledgeStep = (): JSX.Element => {
  const { brainType } = useBrainKnowledgeStep();
  const { currentStepIndex, goToPreviousStep } = useBrainCreationSteps();

  const brainTypeToKnowledgeComponent: Record<BrainType, JSX.Element> = {
    doc: <KnowledgeToFeed hideBrainSelector={true} />,
    api: <ApiRequestDefinition />,
    composite: <CompositeBrainConnections />,
  };

  const previous = (): void => {
    goToPreviousStep();
  };

  const feed = (): void => {
    console.info("hey");
  };

  if (currentStepIndex !== 2 || !brainType) {
    return <></>;
  }

  return (
    <div className={styles.brain_knowledge_wrapper}>
      {brainTypeToKnowledgeComponent[brainType]}
      <div className={styles.buttons_wrapper}>
        <QuivrButton
          label="Previous step"
          color="primary"
          iconName="chevronLeft"
          onClick={previous}
        />
        <QuivrButton
          label="Create brain"
          color="primary"
          iconName="add"
          onClick={feed}
        />
      </div>
    </div>
  );
};
