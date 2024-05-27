import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { useUserApi } from "@/lib/api/user/useUserApi";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useUserData } from "@/lib/hooks/useUserData";

import styles from "./CreateBrainStep.module.scss";
import { useBrainCreationApi } from "./hooks/useBrainCreationApi";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const CreateBrainStep = (): JSX.Element => {
  const { currentStepIndex, goToPreviousStep } = useBrainCreationSteps();
  const { createBrain } = useBrainCreationApi();
  const { creating, setCreating } = useBrainCreationContext();
  const { knowledgeToFeed } = useKnowledgeToFeedContext();
  const { userIdentityData } = useUserData();
  const { updateUserIdentity } = useUserApi();

  const previous = (): void => {
    goToPreviousStep();
  };

  const feed = async (): Promise<void> => {
    if (!userIdentityData?.onboarded) {
      await updateUserIdentity({
        ...userIdentityData,
        username: userIdentityData?.username ?? "",
        onboarded: true,
      });
    }
    setCreating(true);
    createBrain();
  };

  const renderFeedBrain = () => {
    return (
      <>
        {!userIdentityData?.onboarded && (
          <MessageInfoBox type="tutorial">
            <span>
              Upload documents or add URLs to add knowledges to your brain.
            </span>
          </MessageInfoBox>
        )}
        <div>
          <span className={styles.title}>Feed your brain</span>
          <KnowledgeToFeed hideBrainSelector={true} />
        </div>
      </>
    );
  };

  const renderButtons = () => {
    return (
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
          disabled={
            knowledgeToFeed.length === 0 && !userIdentityData?.onboarded
          }
          isLoading={creating}
          important={true}
        />
      </div>
    );
  };

  if (currentStepIndex !== 1) {
    return <></>;
  }

  return (
    <div className={styles.brain_knowledge_wrapper}>
      {renderFeedBrain()}
      {renderButtons()}
    </div>
  );
};
