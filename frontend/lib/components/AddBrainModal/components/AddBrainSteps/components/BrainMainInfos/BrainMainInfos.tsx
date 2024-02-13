import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./BrainMainInfos.module.scss";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainMainInfos = (): JSX.Element => {
  const { currentStepIndex, goToNextStep, goToPreviousStep } =
    useBrainCreationSteps();

  const next = (): void => {
    goToNextStep();
  };

  const previous = (): void => {
    goToPreviousStep();
  };

  if (currentStepIndex !== 1) {
    return <></>;
  }

  return (
    <div className={styles.brain_main_infos_wrapper}>
      <span>Hello</span>
      <div className={styles.buttons_wrapper}>
        <QuivrButton
          color="primary"
          label="Previous Step"
          onClick={() => previous()}
          iconName="chevronLeft"
        />
        <QuivrButton
          color="primary"
          label="Next Step"
          onClick={() => next()}
          iconName="chevronRight"
        />
      </div>
    </div>
  );
};
