import { useUserApi } from "@/lib/api/user/useUserApi";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useUserData } from "@/lib/hooks/useUserData";

import { BrainRecapCard } from "./BrainRecapCard/BrainRecapCard";
import styles from "./BrainRecapStep.module.scss";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";
import { useBrainCreationApi } from "../FeedBrainStep/hooks/useBrainCreationApi";

export const BrainRecapStep = (): JSX.Element => {
  const { currentStepIndex, goToPreviousStep } = useBrainCreationSteps();
  const { creating, setCreating } = useBrainCreationContext();
  const { knowledgeToFeed } = useKnowledgeToFeedContext();
  const { createBrain } = useBrainCreationApi();
  const { updateUserIdentity } = useUserApi();
  const { userIdentityData } = useUserData();

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

  const previous = (): void => {
    goToPreviousStep();
  };

  if (currentStepIndex !== 2) {
    return <></>;
  }

  return (
    <div className={styles.brain_recap_wrapper}>
      <div className={styles.content}>
        <BrainRecapCard label="Connection" number={knowledgeToFeed.length} />
        <BrainRecapCard label="URL" number={knowledgeToFeed.length} />
        <BrainRecapCard label="Document" number={knowledgeToFeed.length} />
      </div>
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
    </div>
  );
};
