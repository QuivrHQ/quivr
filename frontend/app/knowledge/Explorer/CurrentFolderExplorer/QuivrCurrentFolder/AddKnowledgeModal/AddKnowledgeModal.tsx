import { useState } from "react";

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

  const FILE_TYPES = ["pdf", "docx", "doc", "txt"];

  const addKnowledge = () => {
    setLoading(true);
    setIsOpen(false);
    setLoading(false);
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
              onClick={addKnowledge}
              isLoading={loading}
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default AddKnowledgeModal;
