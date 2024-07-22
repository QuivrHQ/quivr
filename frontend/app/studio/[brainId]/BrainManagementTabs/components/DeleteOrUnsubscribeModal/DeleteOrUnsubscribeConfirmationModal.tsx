import { useTranslation } from "react-i18next";

import { Modal } from "@/lib/components/ui/Modal/Modal";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";

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
      size="auto"
      Trigger={<div />}
      CloseTrigger={<div />}
    >
      <div className="flex flex-row justify-center items-center mt-10 gap-20">
        <QuivrButton
          onClick={() => setOpen(false)}
          label={t("returnButton")}
          iconName="chevronLeft"
          color="primary"
        ></QuivrButton>
        <QuivrButton
          onClick={onConfirm}
          isLoading={isDeleteOrUnsubscribeRequestPending}
          color="dangerous"
          iconName="delete"
          label={
            isOwnedByCurrentUser
              ? t("deleteConfirmYes")
              : t("unsubscribeButton")
          }
        ></QuivrButton>
      </div>
    </Modal>
  );
};
