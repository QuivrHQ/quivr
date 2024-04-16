import { useState } from "react";

import { Assistant } from "@/lib/api/assistants/types";
import { Stepper } from "@/lib/components/AddBrainModal/components/Stepper/Stepper";
import { StepValue } from "@/lib/components/AddBrainModal/types/types";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
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
  const [files, setFiles] = useState<{ key: string; file: File | null }[]>(
    assistant.inputs.files.map((fileInput) => ({
      key: fileInput.key,
      file: null,
    }))
  );

  const handleFileChange = (file: File, inputKey: string) => {
    setFiles((prevFiles) =>
      prevFiles.map((fileObj) =>
        fileObj.key === inputKey ? { ...fileObj, file } : fileObj
      )
    );

    console.info(files);
  };

  // const processAssistant = () => {
  //   const res = processAssistant(
  //     {
  //       name: assistant.name,
  //       inputs: {
  //         files: [{ value: file.name, key: inputKey }],
  //         urls: [],
  //         texts: [],
  //       },
  //       outputs: {
  //         email: {
  //           activated: true,
  //         },
  //         brain: {
  //           activated: true,
  //           value: "9654e397-571a-4370-b3e9-0245acc8191a",
  //         },
  //       },
  //     },
  //     [file]
  //   );
  // };

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
          {currentStep === "FIRST_STEP" ? (
            <MessageInfoBox type="info">
              <span className={styles.title}>Expected Input:</span>
              {assistant.input_description}
            </MessageInfoBox>
          ) : (
            <MessageInfoBox type="info">
              <span className={styles.title}>Output:</span>
              {assistant.output_description}
            </MessageInfoBox>
          )}
          {currentStep === "FIRST_STEP" ? (
            <InputsStep
              inputs={assistant.inputs}
              onFileChange={handleFileChange}
            />
          ) : (
            <OutputsStep setEmailOutput={setEmailOutput} />
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
              onClick={() => setCurrentStep("SECOND_STEP")}
              disabled={!!files.find((file) => !file.file)}
            />
          )}
        </div>
      </div>
    </Modal>
  );
};
