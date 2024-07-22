import { useState } from "react";

import { Assistant } from "@/lib/api/assistants/types";
import { useAssistants } from "@/lib/api/assistants/useAssistants";
import { Stepper } from "@/lib/components/AddBrainModal/components/Stepper/Stepper";
import { StepValue } from "@/lib/components/AddBrainModal/types/types";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Step } from "@/lib/types/Modal";

import styles from "./AssistantModal.module.scss";
import { InputsStep } from "./InputsStep/InputsStep";
import { OutputsStep } from "./OutputsStep/OutputsStep";

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
  const [emailOutput, setEmailOutput] = useState<boolean>(true);
  const [brainOutput, setBrainOutput] = useState<string>("");
  const [files, setFiles] = useState<{ key: string; file: File | null }[]>(
    assistant.inputs.files.map((fileInput) => ({
      key: fileInput.key,
      file: null,
    }))
  );
  const { processAssistant } = useAssistants();

  const handleFileChange = (file: File, inputKey: string) => {
    setFiles((prevFiles) =>
      prevFiles.map((fileObj) =>
        fileObj.key === inputKey ? { ...fileObj, file } : fileObj
      )
    );
  };

  const handleSetIsOpen = (value: boolean) => {
    if (!value) {
      setCurrentStep("FIRST_STEP");
    }
    setIsOpen(value);
  };

  const handleProcessAssistant = async () => {
    handleSetIsOpen(false);
    await processAssistant(
      {
        name: assistant.name,
        inputs: {
          files: files.map((file) => ({
            key: file.key,
            value: (file.file as File).name,
          })),
          urls: [],
          texts: [],
        },
        outputs: {
          email: {
            activated: emailOutput,
          },
          brain: {
            activated: brainOutput !== "",
            value: brainOutput,
          },
        },
      },
      files.map((file) => file.file as File)
    );
  };

  return (
    <Modal
      title={assistant.name}
      desc={assistant.description}
      isOpen={isOpen}
      setOpen={handleSetIsOpen}
      size="big"
      CloseTrigger={<div />}
    >
      <div className={styles.modal_content_container}>
        <div className={styles.modal_content_wrapper}>
          <Stepper steps={steps} currentStep={currentStep} />
          {currentStep === "FIRST_STEP" ? (
            <MessageInfoBox type="tutorial">
              <div className={styles.message_wrapper}>
                <span className={styles.title}>Expected Input</span>
                {assistant.input_description}
              </div>
            </MessageInfoBox>
          ) : (
            <MessageInfoBox type="tutorial">
              <div className={styles.message_wrapper}>
                <span className={styles.title}>Output</span>
                {assistant.output_description}
              </div>
            </MessageInfoBox>
          )}
          {currentStep === "FIRST_STEP" ? (
            <InputsStep
              inputs={assistant.inputs}
              onFileChange={handleFileChange}
            />
          ) : (
            <OutputsStep
              setEmailOutput={setEmailOutput}
              setBrainOutput={setBrainOutput}
            />
          )}
        </div>
        <div className={styles.button}>
          {currentStep === "FIRST_STEP" ? (
            <QuivrButton
              label="Next"
              color="primary"
              iconName="chevronRight"
              onClick={() => setCurrentStep("SECOND_STEP")}
              disabled={!!files.find((file) => !file.file)}
            />
          ) : (
            <QuivrButton
              label="Process"
              color="primary"
              iconName="chevronRight"
              onClick={() => handleProcessAssistant()}
              disabled={!emailOutput && brainOutput === ""}
            />
          )}
        </div>
      </div>
    </Modal>
  );
};
