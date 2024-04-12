import { useState } from "react";

import { Assistant } from "@/lib/api/assistants/types";
import { Stepper } from "@/lib/components/AddBrainModal/components/Stepper/Stepper";
import { StepValue } from "@/lib/components/AddBrainModal/types/types";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Step } from "@/lib/types/Modal";

import styles from "./AssistantModal.module.scss";

interface AssistantModalProps {
  isOpen: boolean;
  setIsOpen: (value: boolean) => void;
  assistant: Assistant;
}

export const AssistantModal = ({
  isOpen,
  setIsOpen,
  assistant,
}: AssistantModalProps): JSX.Element => {
  const steps: Step[] = [
    {
      label: "Inputs",
      value: "FIRST_STEP",
    },
    {
      label: "Outputs",
      value: "SECOND_STEP",
    },
  ];
  const [currentStep, setCurrentStep] = useState<StepValue>("FIRST_STEP");

  return (
    <Modal
      title={assistant.name}
      desc={assistant.description}
      isOpen={isOpen}
      setOpen={setIsOpen}
      size="big"
      CloseTrigger={<div />}
    >
      <div className={styles.modal_content_container}>
        <div className={styles.modal_content_wrapper}>
          <Stepper steps={steps} currentStep={currentStep} />
          <MessageInfoBox type="info">
            <span className={styles.title}>Expected Input:</span>
            {assistant.input_description}
          </MessageInfoBox>
        </div>
        <div className={styles.button}>
          <QuivrButton
            label="Next"
            color="primary"
            iconName="chevronRight"
            onClick={() => setCurrentStep("SECOND_STEP")}
          />
        </div>
      </div>
    </Modal>
  );
};
