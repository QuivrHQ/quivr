import { useEffect, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { FileInput } from "@/lib/components/ui/FileInput/FileInput";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { AddKnowledgeData } from "@/lib/types/Knowledge";
import { Tab } from "@/lib/types/Tab";

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
  const [selectedTab, setSelectedTab] = useState<string>("From Documents");
  const [selectedKnowledges, setSelectedKnowledges] = useState<File[]>([]);
  const { addKnowledge } = useKnowledgeApi();

  const FILE_TYPES = ["pdf", "docx", "doc", "txt"];

  const tabs: Tab[] = [
    {
      label: "From Documents",
      isSelected: selectedTab === "From Documents",
      onClick: () => setSelectedTab("From Documents"),
      iconName: "file",
    },
    {
      label: "From URLs",
      isSelected: selectedTab === "From URLs",
      onClick: () => setSelectedTab("From URLs"),
      iconName: "link",
    },
  ];

  const handleAddKnowledge = async () => {
    setLoading(true);
    try {
      await Promise.all(
        files.map(async (file) => {
          try {
            await addKnowledge(
              {
                file_name: file.name,
                parent_id: null,
                is_folder: false,
              } as AddKnowledgeData,
              file
            );
          } catch (error) {
            console.error("Failed to add knowledge:", error);
          }
        })
      );
    } catch (error) {
      console.error("Failed to add all knowledges:", error);
    } finally {
      setLoading(false);
      setIsOpen(false);
      setFiles([]);
      setSelectedKnowledges([]);
    }
  };

  const handleCancel = () => {
    setIsOpen(false);
  };

  const handleFileChange = (newFiles: File[]) => {
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleCheckboxChange = (file: File, checked: boolean) => {
    if (checked) {
      setSelectedKnowledges([...selectedKnowledges, file]);
    } else {
      setSelectedKnowledges(selectedKnowledges.filter((f) => f !== file));
    }
  };

  const handleRemoveSelectedFiles = () => {
    setFiles(files.filter((file) => !selectedKnowledges.includes(file)));
    setSelectedKnowledges([]);
  };

  useEffect(() => {
    if (!isOpen) {
      setFiles([]);
      setSelectedKnowledges([]);
    }
  }, [isOpen]);

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
            <Tabs tabList={tabs} />
            <FileInput
              label="Upload Files"
              onFileChange={handleFileChange}
              acceptedFileTypes={FILE_TYPES}
              hideFileName={true}
              handleMultipleFiles={true}
            />
            {!!files.length && (
              <div className={styles.list_header}>
                <QuivrButton
                  label="Remove"
                  iconName="delete"
                  color="dangerous"
                  onClick={handleRemoveSelectedFiles}
                  disabled={selectedKnowledges.length === 0}
                />
              </div>
            )}
            <div
              className={`${styles.file_list} ${
                !files.length ? styles.empty : ""
              }`}
            >
              {files.map((file, index) => (
                <div key={index} className={styles.file_item}>
                  <Checkbox
                    checked={selectedKnowledges.includes(file)}
                    setChecked={(checked) =>
                      handleCheckboxChange(file, checked)
                    }
                  />
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
              disabled={files.length === 0}
              important={true}
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default AddKnowledgeModal;
