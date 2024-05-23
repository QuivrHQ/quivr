import Image from "next/image";

import { Modal } from "@/lib/components/ui/Modal/Modal";

import styles from "./ConnectionModal.module.scss";

interface ConnectionModalProps {
  modalOpened: boolean;
  setModalOpened: (value: boolean) => void;
  label: string;
  iconUrl: string;
}

export const ConnectionModal = ({
  modalOpened,
  setModalOpened,
  label,
  iconUrl,
}: ConnectionModalProps): JSX.Element => {
  return (
    <div className={styles.connection_modal_wrapper}>
      <Modal
        isOpen={modalOpened}
        setOpen={setModalOpened}
        size="auto"
        CloseTrigger={<div />}
        title={label}
      >
        <div className={styles.modal_wrapper}>
          <div className={styles.subtitle}>
            <Image src={iconUrl} alt={label} width={24} height={24} />
            <span>Add a new {label} connection</span>
          </div>
        </div>
      </Modal>
    </div>
  );
};
