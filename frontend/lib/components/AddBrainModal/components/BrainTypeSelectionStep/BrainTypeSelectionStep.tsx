import { useEffect, useState } from "react";
import { useFormContext } from "react-hook-form";

import { IntegrationBrains } from "@/lib/api/brain/types";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";

import { BrainCatalogue } from "./BrainCatalogue/BrainCatalogue";
import styles from "./BrainTypeSelectionStep.module.scss";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";
import { CreateBrainProps } from "../../types/types";

export const BrainTypeSelectionStep = (): JSX.Element => {
  const [brains, setBrains] = useState<IntegrationBrains[]>([]);
  const { goToNextStep, currentStepIndex } = useBrainCreationSteps();
  const { getIntegrationBrains } = useBrainApi();
  const { setValue } = useFormContext<CreateBrainProps>();

  useEffect(() => {
    getIntegrationBrains()
      .then((response) => {
        setBrains(response);
      })
      .catch((error) => {
        console.error(error);
      });

    setValue("name", "");
    setValue("description", "");
  }, []);

  if (currentStepIndex !== 0) {
    return <></>;
  }

  return (
    <div className={styles.brain_types_wrapper}>
      <div className={styles.main_wrapper}>
        <BrainCatalogue brains={brains} next={goToNextStep} />
      </div>
    </div>
  );
};
