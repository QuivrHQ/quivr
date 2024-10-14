import { useState } from "react";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { Brain } from "@/lib/context/BrainProvider/types";

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
  const [selectedBrains, setSelectedBrains] = useState<Brain[]>([]);

  const handleCheckboxChange = (brain: Brain, checked: boolean) => {
    setSelectedBrains((prevSelectedBrains) => {
      if (checked) {
        return [...prevSelectedBrains, brain];
      } else {
        return prevSelectedBrains.filter((b) => b.id !== brain.id);
      }
    });
  };

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
        <div className={styles.brains_list}>
          {allBrains
            .filter((brain) => brain.brain_type !== "model")
            .map((brain) => (
              <div key={brain.id} className={styles.brain_container}>
                <div className={styles.brain_line}>
                  <Checkbox
                    checked={selectedBrains.some((b) => b.id === brain.id)}
                    setChecked={(checked) =>
                      handleCheckboxChange(brain, checked)
                    }
                  />
                  <div
                    className={styles.sample_wrapper}
                    style={{ backgroundColor: brain.snippet_color }}
                  >
                    <span>{brain.snippet_emoji}</span>
                  </div>
                  <span>{brain.name}</span>
                </div>
              </div>
            ))}
        </div>
      </Modal>
    </div>
  );
};

export default AddToBrainsModal;
