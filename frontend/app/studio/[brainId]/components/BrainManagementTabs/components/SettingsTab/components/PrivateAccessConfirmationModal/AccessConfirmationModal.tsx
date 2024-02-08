import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal/Modal";

import { useBrainFormState } from "../../hooks/useBrainFormState";

type AccessConfirmationModalProps = {
  opened: boolean;
  onClose: () => void;
  onConfirm: () => void;
  onCancel: () => void;
};

export const AccessConfirmationModal = ({
  opened,
  onClose,
  onConfirm,
  onCancel,
}: AccessConfirmationModalProps): JSX.Element => {
  const { t } = useTranslation(["brain"]);
  const { status: selectedStatus } = useBrainFormState();

  const isPrivateStatus = selectedStatus === "private";

  const title = isPrivateStatus
    ? "set_brain_status_to_private_modal_title"
    : "set_brain_status_to_public_modal_title";
  const description = isPrivateStatus
    ? "set_brain_status_to_private_modal_description"
    : "set_brain_status_to_public_modal_description";

  const cancelButtonLabel = isPrivateStatus
    ? "cancel_set_brain_status_to_private"
    : "cancel_set_brain_status_to_public";
  const confirmButtonLabel = isPrivateStatus
    ? "confirm_set_brain_status_to_private"
    : "confirm_set_brain_status_to_public";

  return (
    <Modal isOpen={opened} setOpen={onClose} CloseTrigger={<div />}>
      <div
        dangerouslySetInnerHTML={{
          __html: t(title),
        }}
      />
      <div
        dangerouslySetInnerHTML={{
          __html: t(description),
        }}
      />
      <div className="flex flex-row justify-between pt-10 px-10 items-center">
        <Button type="button" onClick={onConfirm} variant="secondary">
          {t(confirmButtonLabel)}
        </Button>
        <Button type="button" onClick={onCancel}>
          {t(cancelButtonLabel)}
        </Button>
      </div>
    </Modal>
  );
};
