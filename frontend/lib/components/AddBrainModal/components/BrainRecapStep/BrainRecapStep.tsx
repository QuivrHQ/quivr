import { Controller } from "react-hook-form";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { useOnboardingContext } from "@/lib/context/OnboardingProvider/hooks/useOnboardingContext";
import { useUserData } from "@/lib/hooks/useUserData";

import styles from "./BrainRecapStep.module.scss";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";
import { useBrainCreationApi } from "../hooks/useBrainCreationApi";

export const BrainRecapStep = (): JSX.Element => {
  const { currentStepIndex, goToPreviousStep } = useBrainCreationSteps();
  const { creating, setCreating } = useBrainCreationContext();
  const { createBrain } = useBrainCreationApi();
  const { updateUserIdentity } = useUserApi();
  const { userIdentityData } = useUserData();
  const { setIsBrainCreated } = useOnboardingContext();

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
      <div className={styles.content_wrapper}>
        <MessageInfoBox type="warning">
          <span className={styles.warning_message}>
            Depending on the number of knowledge, the upload can take
            <strong> few minutes</strong>.
          </span>
        </MessageInfoBox>
        <span className={styles.title}>Brain Recap</span>
        <div className={styles.brain_info_wrapper}>
          <div className={styles.name_field}>
            <Controller
              name="name"
              render={({ field }) => (
                <TextInput
                  label="Enter your brain name"
                  inputValue={field.value as string}
                  setInputValue={field.onChange}
                  disabled={true}
                />
              )}
            />
          </div>
          <div>
            <Controller
              name="description"
              render={({ field }) => (
                <TextAreaInput
                  label="Enter your brain description"
                  inputValue={field.value as string}
                  setInputValue={field.onChange}
                  disabled={true}
                />
              )}
            />
          </div>
        </div>
        <span className={styles.subtitle}>Knowledge From</span>
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
          onClick={async () => {
            await feed();
            setIsBrainCreated(true);
          }}
          isLoading={creating}
          important={true}
        />
      </div>
    </div>
  );
};
