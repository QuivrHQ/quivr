import { useEffect, useState } from "react";

import { IntegrationBrains } from "@/lib/api/brain/types";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import { BrainCatalogue } from "./BrainCatalogue/BrainCatalogue";
import styles from "./BrainTypeSelectionStep.module.scss";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainTypeSelectionStep = (): JSX.Element => {
  const [brains, setBrains] = useState<IntegrationBrains[]>([]);
  const { goToNextStep, currentStepIndex } = useBrainCreationSteps();
  const { getIntegrationBrains } = useBrainApi();

  useEffect(() => {
    getIntegrationBrains()
      .then((response) => {
        setBrains(response);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  const next = (): void => {
    goToNextStep();
  };

  if (currentStepIndex !== 0) {
    return <></>;
  }

  return (
    <div className={styles.brain_types_wrapper}>
      <div className={styles.main_wrapper}>
        <BrainCatalogue brains={brains} />
      </div>
      <div className={styles.buttons_wrapper}>
        <QuivrButton
          label="Next Step"
          iconName="chevronRight"
          color="primary"
          onClick={() => next()}
        />
      </div>
    </div>
  );
};
