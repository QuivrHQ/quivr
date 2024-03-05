import { capitalCase } from "change-case";
import { useEffect } from "react";

import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./CreateBrainStep.module.scss";
import { useBrainCreationApi } from "./hooks/useBrainCreationApi";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const CreateBrainStep = (): JSX.Element => {
  const { currentStepIndex, goToPreviousStep } = useBrainCreationSteps();
  const { createBrain, fields, setFields } = useBrainCreationApi();
  const { creating, setCreating, currentSelectedBrain } =
    useBrainCreationContext();

  useEffect(() => {
    if (currentSelectedBrain?.connection_settings) {
      const newFields = Object.entries(
        currentSelectedBrain.connection_settings
      ).map(([key, type]) => {
        return { name: key, type, value: "" };
      });
      setFields(newFields);
    }
  }, [currentSelectedBrain?.connection_settings]);

  const handleInputChange = (name: string, value: string) => {
    setFields(
      fields.map((field) => (field.name === name ? { ...field, value } : field))
    );
  };

  const previous = (): void => {
    goToPreviousStep();
  };

  const feed = (): void => {
    setCreating(true);
    createBrain();
  };

  if (currentStepIndex !== 2) {
    return <></>;
  }

  return (
    <div className={styles.brain_knowledge_wrapper}>
      {fields.map(({ name, value }) => (
        <TextInput
          key={name}
          inputValue={value}
          setInputValue={(inputValue) => handleInputChange(name, inputValue)}
          label={capitalCase(name)}
        />
      ))}
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
