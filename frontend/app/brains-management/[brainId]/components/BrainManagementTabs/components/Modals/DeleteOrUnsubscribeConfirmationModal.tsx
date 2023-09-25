import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal";

type DeleteOrUnsubscribeConfirmationModalProps = {
  isOpen: boolean;
  setOpen: (isOpen: boolean) => void;
  onConfirm: () => void;
  isOwnedByCurrentUser: boolean;
  isDeleteOrUnsubscribeRequestPending: boolean;
};

export const DeleteOrUnsubscribeConfirmationModal = ({
  isOpen,
  setOpen,
  onConfirm,
  isOwnedByCurrentUser,
  isDeleteOrUnsubscribeRequestPending,
}: DeleteOrUnsubscribeConfirmationModalProps): JSX.Element => {
  const { t } = useTranslation(["delete_or_unsubscribe_from_brain"]);

  return (
    <Modal
      desc={
        isOwnedByCurrentUser
          ? t("deleteConfirmQuestion")
          : t("unsubscribeConfirmQuestion")
      }
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
            onClick={onConfirm}
            isLoading={isDeleteOrUnsubscribeRequestPending}
          >
            {isOwnedByCurrentUser
              ? t("deleteConfirmYes")
              : t("unsubscribeButton")}
          </Button>
        </div>
      </div>
    </Modal>
  );
};
