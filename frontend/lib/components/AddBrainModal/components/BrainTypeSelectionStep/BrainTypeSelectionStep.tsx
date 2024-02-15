import { useState } from "react";

import { BrainType } from "@/lib/components/AddBrainModal/types/types";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import { BrainTypeSelection } from "./BrainTypeSelection/BrainTypeSelection";
import styles from "./BrainTypeSelectionStep.module.scss";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainTypeSelectionStep = (): JSX.Element => {
  const [selectedIndex, setSelectedIndex] = useState<number>(0);
  const { goToNextStep, currentStepIndex } = useBrainCreationSteps();

  const brainTypes: BrainType[] = [
    {
      name: "Core Brain",
      description: "Upload documents or website links to feed your brain.",
      iconName: "feed",
    },
    {
      name: "Sync Brain - Coming soon!",
      description:
        "Connect to your tools and applications to interact with your data.",
      iconName: "software",
      disabled: true,
    },
    {
      name: "Custom Brain - Coming soon!",
      description:
        "Explore your databases, converse with your APIs, and much more!",
      iconName: "custom",
      disabled: true,
    },
  ];

  const next = (): void => {
    goToNextStep();
  };

  if (currentStepIndex !== 0) {
    return <></>;
  }

  return (
    <div className={styles.brain_types_wrapper}>
      <div className={styles.main_wrapper}>
        <span className={styles.title}>Choose a type of brain</span>
        {brainTypes.map((brainType, index) => (
          <div key={index}>
            <BrainTypeSelection
              brainType={brainType}
              selected={index === selectedIndex}
              onClick={() => setSelectedIndex(index)}
            />
          </div>
        ))}
      </div>
      <div className={styles.button}>
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
