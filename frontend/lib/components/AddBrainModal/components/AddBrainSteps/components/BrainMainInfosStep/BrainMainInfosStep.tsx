import { useEffect, useState } from "react";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./BrainMainInfosStep.module.scss";

import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainMainInfosStep = (): JSX.Element => {
  const { currentStepIndex, goToNextStep, goToPreviousStep } =
    useBrainCreationSteps();

  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [completed, setCompleted] = useState<boolean>(false);

  const next = (): void => {
    goToNextStep();
  };

  const previous = (): void => {
    goToPreviousStep();
  };

  useEffect(() => {
    if (!!name && !!description) {
      setCompleted(true);
    } else {
      setCompleted(false);
    }
  }, [name, description]);

  if (currentStepIndex !== 1) {
    return <></>;
  }

  return (
    <div className={styles.brain_main_infos_wrapper}>
      <div className={styles.inputs_wrapper}>
        <TextInput label="Name" inputValue={name} setInputValue={setName} />
        <TextAreaInput
          label="Description"
          inputValue={description}
          setInputValue={setDescription}
        />
      </div>
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
          disabled={!completed}
        />
      </div>
    </div>
  );
};
