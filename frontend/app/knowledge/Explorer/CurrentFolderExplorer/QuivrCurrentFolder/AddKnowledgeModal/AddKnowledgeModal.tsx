import { useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { FileInput } from "@/lib/components/ui/FileInput/FileInput";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./AddKnowledgeModal.module.scss";

interface AddKnowledgeModalProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const AddKnowledgeModal = ({
  isOpen,
  setIsOpen,
}: AddKnowledgeModalProps): JSX.Element => {
  const [loading, setLoading] = useState<boolean>(false);
  const [files, setFiles] = useState<File[]>([]);
  const { addKnowledge } = useKnowledgeApi();

  const FILE_TYPES = ["pdf", "docx", "doc", "txt"];

  const handleAddKnowledge = () => {
    setLoading(true);
    files.map(async (file) => {
      try {
        await addKnowledge(
          {
            file_name: file.name,
            parent_id: null,
            is_folder: false,
          },
          file
        );
      } catch (error) {
        console.error("Failed to add knowledge:", error);
      }
    });

    // setIsOpen(false);
    // setLoading(false);
  };

  const handleCancel = () => {
    setIsOpen(false);
  };

  const handleFileChange = (file: File) => {
    setFiles([...files, file]);
  };

  return (
    <div className={styles.main_container}>
      <Modal
        title="Add Knowledge"
        isOpen={isOpen}
        setOpen={setIsOpen}
        size="big"
        Trigger={<div />}
        CloseTrigger={<div />}
      >
        <div className={styles.modal_content}>
          <div className={styles.top}>
            <FileInput
              label="Upload Files"
              onFileChange={handleFileChange}
              acceptedFileTypes={FILE_TYPES}
              hideFileName={true}
            />
            <div className={styles.file_list}>
              {files.map((file, index) => (
                <div key={index} className={styles.file_item}>
                  <span>{file.name}</span>
                </div>
              ))}
            </div>
          </div>
          <div className={styles.buttons_wrapper}>
            <QuivrButton
              label="Cancel"
              iconName="close"
              color="dangerous"
              onClick={handleCancel}
            />
            <QuivrButton
              label="Add Knowledge"
              iconName="add"
              color="primary"
              onClick={handleAddKnowledge}
              isLoading={loading}
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default AddKnowledgeModal;
