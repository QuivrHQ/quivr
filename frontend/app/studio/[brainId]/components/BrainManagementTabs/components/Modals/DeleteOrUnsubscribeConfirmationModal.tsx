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
      CloseTrigger={<div />}
    >
      <div className="flex flex-row justify-center items-center mt-10 gap-20">
        <Button onClick={() => setOpen(false)} data-testid="return-button">
          {t("returnButton")}
        </Button>
        <Button
          data-testid="delete-brain"
          className="px-4 bg-red-500 text-white"
          onClick={onConfirm}
          isLoading={isDeleteOrUnsubscribeRequestPending}
        >
          {isOwnedByCurrentUser
            ? t("deleteConfirmYes")
            : t("unsubscribeButton")}
        </Button>
      </div>
    </Modal>
  );
};
