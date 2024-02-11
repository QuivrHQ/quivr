import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal/Modal";

type PublicAccessConfirmationModalProps = {
  opened: boolean;
  onClose: () => void;
  onConfirm: () => void;
  onCancel: () => void;
};
export const PublicAccessConfirmationModal = ({
  opened,
  onClose,
  onConfirm,
  onCancel,
}: PublicAccessConfirmationModalProps): JSX.Element => {
  const { t } = useTranslation(["brain"]);

  return (
    <Modal isOpen={opened} setOpen={onClose} CloseTrigger={<div />}>
      <div
        dangerouslySetInnerHTML={{
          __html: t("set_brain_status_to_public_modal_title"),
        }}
      />
      <div
        dangerouslySetInnerHTML={{
          __html: t("set_brain_status_to_public_modal_description"),
        }}
      />
      <div className="flex flex-row justify-between pt-10 px-10 items-center">
        <Button type="button" onClick={onConfirm} variant="secondary">
          {t("confirm_set_brain_status_to_public")}
        </Button>
        <Button type="button" onClick={onCancel}>
          {t("cancel_set_brain_status_to_public")}
        </Button>
      </div>
    </Modal>
  );
};
