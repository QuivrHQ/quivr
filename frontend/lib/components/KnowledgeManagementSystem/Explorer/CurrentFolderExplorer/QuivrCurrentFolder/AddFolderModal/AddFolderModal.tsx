import { useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { useKnowledgeContext } from "@/lib/components/KnowledgeManagementSystem/KnowledgeProvider/hooks/useKnowledgeContext";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./AddFolderModal.module.scss";

interface AddFolderModalProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const AddFolderModal = ({
  isOpen,
  setIsOpen,
}: AddFolderModalProps): JSX.Element => {
  const [folderName, setFolderName] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const { currentFolder, setRefetchFolderMenu } = useKnowledgeContext();
  const { addFolder } = useKnowledgeApi();

  const handleKeyDown = async (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && folderName !== "") {
      await createFolder();
    }
  };

  const createFolder = async () => {
    if (folderName !== "") {
      setLoading(true);
      await addFolder({
        parent_id: currentFolder?.id ?? null,
        file_name: folderName,
        is_folder: true,
      });
      setRefetchFolderMenu(true);
      setFolderName("");
      setIsOpen(false);
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setFolderName("");
    setIsOpen(false);
  };

  return (
    <div className={styles.main_container}>
      <Modal
        title="Add Folder"
        isOpen={isOpen}
        setOpen={setIsOpen}
        size="auto"
        Trigger={<div />}
        CloseTrigger={<div />}
      >
        <div className={styles.modal_content}>
          <TextInput
            label="Folder Name"
            iconName="folder"
            inputValue={folderName}
            setInputValue={setFolderName}
            onKeyDown={(event) => void handleKeyDown(event)}
          />
          <div className={styles.buttons_wrapper}>
            <QuivrButton
              label="Cancel"
              iconName="close"
              color="dangerous"
              onClick={handleCancel}
            />
            <QuivrButton
              label="Create Folder"
              iconName="add"
              color="primary"
              disabled={folderName === ""}
              onClick={createFolder}
              isLoading={loading}
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default AddFolderModal;
