import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./CreateBrainStep.module.scss";
import { useBrainCreationApi } from "./hooks/useBrainCreationApi";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const CreateBrainStep = (): JSX.Element => {
  const { currentStepIndex, goToPreviousStep } = useBrainCreationSteps();
  const { createBrain } = useBrainCreationApi();
  const { creating, setCreating, currentIntegrationBrain } =
    useBrainCreationContext();

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
      {!currentIntegrationBrain ? (
        <div>
          <span className={styles.title}>Feed your brain</span>
          <KnowledgeToFeed hideBrainSelector={true} />
        </div>
      ) : (
        <div className={styles.message_info_box_wrapper}>
          <MessageInfoBox type="info">
            <div className={styles.message_content}>
              Click on
              <QuivrButton
                label="Create"
                color="primary"
                iconName="add"
                onClick={feed}
                isLoading={creating}
              />
              to finish your brain creation.
            </div>
          </MessageInfoBox>
        </div>
      )}
      <div className={styles.buttons_wrapper}>
        <QuivrButton
          label="Previous step"
          color="primary"
          iconName="chevronLeft"
          onClick={previous}
        />
        <QuivrButton
          label="Create"
          color="primary"
          iconName="add"
          onClick={feed}
          isLoading={creating}
        />
      </div>
    </div>
  );
};
