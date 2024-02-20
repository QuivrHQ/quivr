import { useEffect, useState } from "react";

import { IntegrationBrains } from "@/lib/api/brain/types";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { BrainType } from "@/lib/components/AddBrainModal/types/types";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import { BrainTypeSelection } from "./BrainTypeSelection/BrainTypeSelection";
import styles from "./BrainTypeSelectionStep.module.scss";
import { CustomBrainList } from "./CustomBrainList/CustomBrainList";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainTypeSelectionStep = (): JSX.Element => {
  const [selectedIndex, setSelectedIndex] = useState<number>(0);
  const [customBrainsCatalogueOpened, setCustomBrainsCatalogueOpened] =
    useState<boolean>(false);
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

  const brainTypes: BrainType[] = [
    {
      name: "Core Brain",
      description: "Upload documents or website links to feed your brain.",
      iconName: "feed",
    },
    {
      name: "Custom Brain",
      description:
        "Explore your databases, converse with your APIs, and much more!",
      iconName: "custom",
      onClick: () => {
        setCustomBrainsCatalogueOpened(true);
      },
    },
    {
      name: "Sync Brain - Coming soon!",
      description:
        "Connect to your tools and applications to interact with your data.",
      iconName: "software",
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
        {customBrainsCatalogueOpened ? (
          <CustomBrainList customBrainList={customBrains} />
        ) : (
          <>
            <span className={styles.title}>Choose a type of brain</span>
            {brainTypes.map((brainType, index) => (
              <div key={index}>
                <BrainTypeSelection
                  brainType={brainType}
                  selected={index === selectedIndex}
                  onClick={() => {
                    setSelectedIndex(index);
                    if (brainType.onClick) {
                      brainType.onClick();
                    }
                  }}
                />
              </div>
            ))}
          </>
        )}
      </div>
      <div
        className={`${styles.buttons_wrapper} ${
          customBrainsCatalogueOpened ? styles.two_buttons : ""
        }`}
      >
        {customBrainsCatalogueOpened && (
          <QuivrButton
            label="Type of brain"
            iconName="chevronLeft"
            color="primary"
            onClick={() => {
              setCustomBrainsCatalogueOpened(false);
              setSelectedIndex(-1);
            }}
          />
        )}
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
