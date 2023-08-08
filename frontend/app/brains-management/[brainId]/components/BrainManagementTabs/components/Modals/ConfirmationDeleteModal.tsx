import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal";

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
  const { t } = useTranslation(["delete_brain"]);

  return (
    <Modal
      desc={t("deleteConfirmQuestion")}
      isOpen={isOpen}
      setOpen={setOpen}
      Trigger={<div />}
      CloseTrigger={
        <Button className="self-end" data-testid="return-button">
          {t("returnButton")}
        </Button>
      }
    >
      <div>
        <div className="flex justify-center mt-6">
          <Button
            data-testid="delete-brain"
            className="px-4 py-2 bg-red-500 text-white rounded-md"
            onClick={onDelete}
          >
            {t("deleteConfirmYes")}
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default ConfirmationDeleteModal;
