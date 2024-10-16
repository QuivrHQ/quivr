import { useEffect, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { KMSElement } from "@/lib/api/sync/types";
import { useKnowledgeContext } from "@/lib/components/KnowledgeManagementSystem/KnowledgeProvider/hooks/useKnowledgeContext";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { Brain } from "@/lib/context/BrainProvider/types";

import styles from "./AddToBrainsModal.module.scss";

interface AddToBrainsModalProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
  knowledge?: KMSElement;
}

const AddToBrainsModal = ({
  isOpen,
  setIsOpen,
  knowledge,
}: AddToBrainsModalProps): JSX.Element => {
  const [selectedBrains, setSelectedBrains] = useState<Brain[]>([]);
  const [initialBrains, setInitialBrains] = useState<Brain[]>([]);
  const [saveLoading, setSaveLoading] = useState(false);

  const { allBrains } = useBrainContext();
  const { linkKnowledgeToBrains, unlinkKnowledgeFromBrains } =
    useKnowledgeApi();
  const { setRefetchFolderExplorer } = useKnowledgeContext();

  useEffect(() => {
    if (knowledge) {
      const initialSelectedBrains = allBrains.filter((brain) =>
        knowledge.brains.some((kb) => kb.brain_id === brain.id)
      );
      setSelectedBrains(initialSelectedBrains);
      setInitialBrains(initialSelectedBrains);
    }
  }, [knowledge, allBrains]);

  const handleCheckboxChange = (brain: Brain, checked: boolean) => {
    setSelectedBrains((prevSelectedBrains) => {
      return checked
        ? [...prevSelectedBrains, brain]
        : prevSelectedBrains.filter((b) => b.id !== brain.id);
    });
  };

  const hasChanges = () => {
    if (selectedBrains.length !== initialBrains.length) {
      return true;
    }
    const selectedBrainIds = selectedBrains.map((b) => b.id).sort();
    const initialBrainIds = initialBrains.map((b) => b.id).sort();

    return !selectedBrainIds.every(
      (id, index) => id === initialBrainIds[index]
    );
  };

  const updateConnectedBrains = async () => {
    if (!knowledge) {
      return;
    }

    const knowledgeId = knowledge.id;
    const brainIdsToLink = selectedBrains.map((brain) => brain.id);
    const brainIdsToUnlink = initialBrains
      .filter((brain) => !selectedBrains.some((b) => b.id === brain.id))
      .map((brain) => brain.id);

    try {
      setSaveLoading(true);
      if (brainIdsToLink.length > 0) {
        await linkKnowledgeToBrains(knowledge, brainIdsToLink);
      }
      if (brainIdsToUnlink.length > 0) {
        await unlinkKnowledgeFromBrains(knowledgeId, brainIdsToUnlink);
      }
    } catch (error) {
      console.error("Failed to update knowledge to brains", error);
    } finally {
      setSaveLoading(false);
      setIsOpen(false);
      setRefetchFolderExplorer(true);
    }
  };

  return (
    <div
      className={styles.main_container}
      onClick={(event) => event.stopPropagation()}
    >
      <Modal
        title="Add Knowledge To Brains"
        isOpen={isOpen}
        setOpen={setIsOpen}
        size="auto"
        Trigger={<div />}
        CloseTrigger={<div />}
      >
        <div className={styles.content_wrapper}>
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
          <div className={styles.button}>
            <QuivrButton
              label="Save"
              important={true}
              color="primary"
              iconName="upload"
              disabled={!hasChanges()}
              onClick={updateConnectedBrains}
              isLoading={saveLoading}
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default AddToBrainsModal;
