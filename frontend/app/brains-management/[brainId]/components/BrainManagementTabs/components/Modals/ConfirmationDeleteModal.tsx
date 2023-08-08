import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal";

const CONFIRMATION_DELETE_QUESTION =
  "Are you sure you want to delete this brain? This action cannot be undone.";
const CONFIRMATION_DELETE_BUTTON = "Confirm Delete";
const CONFIRMATION_DELETE_RETURN_BUTTON = "Return";

type ConfirmationDeleteModalProps = {
  isOpen: boolean;
  setOpen: (isOpen: boolean) => void;
  onDelete: () => void;
};

const ConfirmationDeleteModal = ({
  isOpen,
  setOpen,
  onDelete,
}: ConfirmationDeleteModalProps): JSX.Element => {
  return (
    <Modal
      desc={CONFIRMATION_DELETE_QUESTION}
      isOpen={isOpen}
      setOpen={setOpen}
      Trigger={<div />}
      CloseTrigger={
        <Button className="self-end">
          {CONFIRMATION_DELETE_RETURN_BUTTON}
        </Button>
      }
    >
      <div>
        <div className="flex justify-center mt-6">
          <Button
            className="px-4 py-2 bg-red-500 text-white rounded-md"
            onClick={onDelete}
          >
            {CONFIRMATION_DELETE_BUTTON}
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default ConfirmationDeleteModal;
