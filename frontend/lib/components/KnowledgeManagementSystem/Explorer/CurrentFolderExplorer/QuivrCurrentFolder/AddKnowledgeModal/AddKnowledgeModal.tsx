import { useEffect, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { useKnowledgeContext } from "@/lib/components/KnowledgeManagementSystem/KnowledgeProvider/hooks/useKnowledgeContext";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { FileInput } from "@/lib/components/ui/FileInput/FileInput";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import {
  AddKnowledgeFileData,
  AddKnowledgeUrlData,
} from "@/lib/types/Knowledge";
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
  const [currentUrl, setCurrentUrl] = useState<string>("");
  const [files, setFiles] = useState<File[]>([]);
  const [urls, setUrls] = useState<string[]>([]);
  const [selectedTab, setSelectedTab] = useState<string>("Documents");
  const [selectedKnowledges, setSelectedKnowledges] = useState<
    (File | string)[]
  >([]);
  const { addKnowledgeFile, addKnowledgeUrl } = useKnowledgeApi();
  const { currentFolder, setRefetchFolderExplorer } = useKnowledgeContext();

  const FILE_TYPES = ["pdf", "docx", "doc", "txt"];

  const tabs: Tab[] = [
    {
      label: "Documents",
      isSelected: selectedTab === "Documents",
      onClick: () => setSelectedTab("Documents"),
      iconName: "file",
    },
    {
      label: "Websites' pages",
      isSelected: selectedTab === "Websites",
      onClick: () => setSelectedTab("Websites"),
      iconName: "link",
    },
  ];

  const handleAddKnowledge = async () => {
    setLoading(true);
    try {
      await Promise.all(
        files.map(async (file) => {
          try {
            await addKnowledgeFile(
              {
                file_name: file.name,
                parent_id: currentFolder?.id ?? null,
                is_folder: false,
              } as AddKnowledgeFileData,
              file
            );
          } catch (error) {
            console.error("Failed to add knowledge:", error);
          }
        })
      );

      await Promise.all(
        urls.map(async (url) => {
          try {
            await addKnowledgeUrl({
              url: url,
              parent_id: currentFolder?.id ?? null,
              is_folder: false,
            } as AddKnowledgeUrlData);
          } catch (error) {
            console.error("Failed to add knowledge from URL:", error);
          }
        })
      );
    } catch (error) {
      console.error("Failed to add all knowledges:", error);
    } finally {
      setLoading(false);
      setIsOpen(false);
      setFiles([]);
      setUrls([]);
      setSelectedKnowledges([]);
      setCurrentUrl("");
      setRefetchFolderExplorer(true);
    }
  };

  const handleCancel = () => {
    setIsOpen(false);
  };

  const handleFileChange = (newFiles: File[]) => {
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleCheckboxChange = (item: File | string, checked: boolean) => {
    if (checked) {
      setSelectedKnowledges([...selectedKnowledges, item]);
    } else {
      setSelectedKnowledges(selectedKnowledges.filter((f) => f !== item));
    }
  };

  const handleRemoveSelectedItems = () => {
    setFiles(files.filter((file) => !selectedKnowledges.includes(file)));
    setUrls(urls.filter((url) => !selectedKnowledges.includes(url)));
    setSelectedKnowledges([]);
  };

  useEffect(() => {
    if (!isOpen) {
      setFiles([]);
      setUrls([]);
      setSelectedKnowledges([]);
      setCurrentUrl("");
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
            <div className={styles.inputs_wrapper}>
              {selectedTab === "Documents" && (
                <FileInput
                  label="Upload Files"
                  onFileChange={handleFileChange}
                  acceptedFileTypes={FILE_TYPES}
                  hideFileName={true}
                  handleMultipleFiles={true}
                />
              )}
              {selectedTab === "Websites" && (
                <div className={styles.url_input}>
                  <TextInput
                    label="URL"
                    inputValue={currentUrl}
                    setInputValue={setCurrentUrl}
                    iconName="followUp"
                    url={true}
                    onSubmit={() => {
                      setCurrentUrl("");
                      setUrls((prevUrls) => [...prevUrls, currentUrl]);
                    }}
                  />
                </div>
              )}
            </div>
            {(!!files.length || !!urls.length) && (
              <div className={styles.list_header}>
                <QuivrButton
                  label="Remove"
                  iconName="delete"
                  color="dangerous"
                  onClick={handleRemoveSelectedItems}
                  disabled={selectedKnowledges.length === 0}
                />
              </div>
            )}
            <div
              className={`${styles.file_list} ${
                !files.length && !urls.length ? styles.empty : ""
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
              {urls.map((url, index) => (
                <div key={index} className={styles.file_item}>
                  <Checkbox
                    checked={selectedKnowledges.includes(url)}
                    setChecked={(checked) => handleCheckboxChange(url, checked)}
                  />
                  <span>{url}</span>
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
              disabled={files.length === 0 && urls.length === 0}
              important={true}
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default AddKnowledgeModal;
