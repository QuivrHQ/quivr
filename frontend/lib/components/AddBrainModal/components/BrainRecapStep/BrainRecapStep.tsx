import styles from "./BrainRecapStep.module.scss";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainRecapStep = (): JSX.Element => {
  const { currentStepIndex } = useBrainCreationSteps();

  if (currentStepIndex !== 2) {
    return <></>;
  }

  return <div className={styles.brain_knowledge_wrapper}>RECAP</div>;
};
