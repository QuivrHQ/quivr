import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./BrainKnowledgeStep.module.scss";
import { useBrainCreationApi } from "./hooks/useBrainCreationApi";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainKnowledgeStep = (): JSX.Element => {
  const { currentStepIndex, goToPreviousStep } = useBrainCreationSteps();
  const { createBrain } = useBrainCreationApi();
  const { creating, setCreating } = useBrainCreationContext();

  const previous = (): void => {
    goToPreviousStep();
  };

  const feed = (): void => {
    setCreating(true);
    createBrain();
  };

  if (currentStepIndex !== 2) {
    return <></>;
  }

  return (
    <div className={styles.brain_knowledge_wrapper}>
      <div>
        <span className={styles.title}>Feed your brain</span>
        <KnowledgeToFeed hideBrainSelector={true} />
      </div>
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
          isLoading={creating}
        />
      </div>
    </div>
  );
};
