import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./BrainKnowledgeStep.module.scss";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainKnowledgeStep = (): JSX.Element => {
  const { currentStepIndex, goToPreviousStep } = useBrainCreationSteps();

  const previous = (): void => {
    goToPreviousStep();
  };

  const feed = (): void => {
    console.info("hey");
  };

  if (currentStepIndex !== 2) {
    return <></>;
  }

  return (
    <div className={styles.brain_knowledge_wrapper}>
      <KnowledgeToFeed hideBrainSelector={true} />
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
