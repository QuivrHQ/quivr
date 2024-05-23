import Image from "next/image";
import { useState } from "react";

import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

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
  const [connectionName, setConnectionName] = useState<string>("");

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
          <TextInput
            label={`${label} connection`}
            inputValue={connectionName}
            setInputValue={setConnectionName}
          />
          <div className={styles.button_wrapper}>
            <QuivrButton
              iconName="sync"
              label="Connect"
              color="primary"
              disabled={!connectionName}
              onClick={() => {
                console.info("hey");
              }}
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};
