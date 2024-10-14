import { Modal } from "@/lib/components/ui/Modal/Modal";

import styles from "./AddToBrainsModal.module.scss";

interface AddToBrainsModalProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const AddToBrainsModal = ({
  isOpen,
  setIsOpen,
}: AddToBrainsModalProps): JSX.Element => {
  return (
    <div className={styles.main_container}>
      <Modal
        title="Add Knowledge To Brains"
        isOpen={isOpen}
        setOpen={setIsOpen}
        size="big"
        Trigger={<div />}
        CloseTrigger={<div />}
      >
        u
      </Modal>
    </div>
  );
};

export default AddToBrainsModal;
