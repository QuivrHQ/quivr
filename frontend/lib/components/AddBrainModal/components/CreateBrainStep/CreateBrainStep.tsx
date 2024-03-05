import { useState } from "react";

import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./CreateBrainStep.module.scss";
import { useBrainCreationApi } from "./hooks/useBrainCreationApi";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const CreateBrainStep = (): JSX.Element => {
  const [settingsValues, setSettingsValues] = useState({});
  const { currentStepIndex, goToPreviousStep } = useBrainCreationSteps();
  const { createBrain } = useBrainCreationApi();
  const { creating, setCreating, currentSelectedBrain } =
    useBrainCreationContext();

  const previous = (): void => {
    console.info(currentSelectedBrain);
    goToPreviousStep();
  };

  const feed = (): void => {
    setCreating(true);
    createBrain();
  };

  const handleInputChange = (key: string, newValue: string) => {
    setSettingsValues((prevValues) => ({
      ...prevValues,
      [key]: newValue,
    }));
  };

  if (currentSelectedBrain) {
    console.info(
      JSON.parse(JSON.stringify(currentSelectedBrain.connection_settings))
    );
  }

  if (currentStepIndex !== 2) {
    return <></>;
  }

  return (
    <div className={styles.brain_knowledge_wrapper}>
      {currentSelectedBrain?.max_files ? (
        <div>
          <span className={styles.title}>Feed your brain</span>
          <KnowledgeToFeed hideBrainSelector={true} />
        </div>
      ) : (
        <div className={styles.message_info_box_wrapper}>
          <MessageInfoBox type="info">
            <div className={styles.message_content}>
              Click on
              <QuivrButton
                label="Create"
                color="primary"
                iconName="add"
                onClick={feed}
                isLoading={creating}
              />
              to finish your brain creation.
            </div>
          </MessageInfoBox>
        </div>
      )}
      {currentSelectedBrain?.connections_settings && (
        <div>
          {Object.entries(currentSelectedBrain.connections_settings).map(
            ([key, type]) => (
              <div key={key}>
                <label>{key}</label>
                <input
                  type={type === "string" ? "text" : "number"}
                  value={settingsValues[key] || ""}
                  onChange={(e) => handleInputChange(key, e.target.value)}
                />
              </div>
            )
          )}
        </div>
      )}
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
          isLoading={creating}
        />
      </div>
    </div>
  );
};
