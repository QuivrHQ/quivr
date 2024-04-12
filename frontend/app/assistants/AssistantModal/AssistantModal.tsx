import { Assistant } from "@/lib/api/assistants/types";
import { Modal } from "@/lib/components/ui/Modal/Modal";

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
  return (
    <Modal
      title={assistant.name}
      desc={assistant.description}
      isOpen={isOpen}
      setOpen={setIsOpen}
      CloseTrigger={<div />}
    ></Modal>
  );
};
