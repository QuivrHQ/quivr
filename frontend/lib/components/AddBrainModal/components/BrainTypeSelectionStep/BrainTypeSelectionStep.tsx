import { useEffect, useState } from "react";

import { IntegrationBrains } from "@/lib/api/brain/types";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./BrainTypeSelectionStep.module.scss";
import { CustomBrainList } from "./CustomBrainList/CustomBrainList";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainTypeSelectionStep = (): JSX.Element => {
  const [selectedIndex] = useState<number>(-1);
  const [customBrainsCatalogueOpened] = useState<boolean>(false);
  const [customBrains, setCustomBrains] = useState<IntegrationBrains[]>([]);
  const { goToNextStep, currentStepIndex } = useBrainCreationSteps();
  const { getIntegrationBrains } = useBrainApi();
  const { currentIntegrationBrain } = useBrainCreationContext();

  useEffect(() => {
    getIntegrationBrains()
      .then((response) => {
        setCustomBrains(
          response.filter((brain) => brain.integration_type === "custom")
        );
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
        <CustomBrainList customBrainList={customBrains} />
      </div>
      <div
        className={`${styles.buttons_wrapper} ${
          customBrainsCatalogueOpened ? styles.two_buttons : ""
        }`}
      >
        <QuivrButton
          label="Next Step"
          iconName="chevronRight"
          color="primary"
          onClick={() => next()}
          disabled={
            selectedIndex === -1 ||
            (!!customBrainsCatalogueOpened && !currentIntegrationBrain)
          }
        />
      </div>
    </div>
  );
};
