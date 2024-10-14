import { Modal } from "@/lib/components/ui/Modal/Modal";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./AddToBrainsModal.module.scss";

interface AddToBrainsModalProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const AddToBrainsModal = ({
  isOpen,
  setIsOpen,
}: AddToBrainsModalProps): JSX.Element => {
  const { allBrains } = useBrainContext();

  console.info(allBrains);

  return (
    <div className={styles.main_container}>
      <Modal
        title="Add Knowledge To Brains"
        isOpen={isOpen}
        setOpen={setIsOpen}
        size="auto"
        Trigger={<div />}
        CloseTrigger={<div />}
      >
        {allBrains
          .filter((brain) => brain.brain_type !== "model")
          .map((brain) => (
            <div key={brain.id} className={styles.brain_container}>
              <div className={styles.brain_name}>
                {brain.display_name ?? brain.name}
              </div>
            </div>
          ))}
      </Modal>
    </div>
  );
};

export default AddToBrainsModal;
