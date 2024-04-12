import { Assistant } from "@/lib/api/assistants/types";
import { Stepper } from "@/lib/components/AddBrainModal/components/Stepper/Stepper";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import { Step } from "@/lib/types/Modal";

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
  const currentStep = "INPUTS";

  return (
    <Modal
      title={assistant.name}
      desc={assistant.description}
      isOpen={isOpen}
      setOpen={setIsOpen}
      size="big"
      CloseTrigger={<div />}
    >
      <>
        <Stepper steps={steps} currentStep={currentStep} />
      </>
    </Modal>
  );
};
