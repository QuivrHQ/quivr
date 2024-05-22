import { Modal } from "@/lib/components/ui/Modal/Modal";

import styles from "./ConnectionModal.module.scss";

interface ConnectionModalProps {
  modalOpened: boolean;
  setModalOpened: (value: boolean) => void;
}

export const ConnectionModal = ({
  modalOpened,
  setModalOpened,
}: ConnectionModalProps): JSX.Element => {
  return (
    <div className={styles.connection_modal_wrapper}>
      <Modal
        isOpen={modalOpened}
        setOpen={setModalOpened}
        size="auto"
        CloseTrigger={<div />}
      >
        <div className={styles.modal_wrapper}>Modal</div>
      </Modal>
    </div>
  );
};
