"use client";

import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./FolderExplorerHeader.module.scss";

import { useKnowledgeContext } from "../../KnowledgeProvider/hooks/useKnowledgeContext";

const FolderExplorerHeader = (): JSX.Element => {
  const { currentFolder, setCurrentFolder } = useKnowledgeContext();

  const loadParentFolder = () => {
    if (currentFolder?.parentKMSElement) {
      setCurrentFolder({
        ...currentFolder.parentKMSElement,
        parentKMSElement: currentFolder.parentKMSElement.parentKMSElement,
      });
    }
  };

  return (
    <div className={styles.header_wrapper}>
      {currentFolder?.parentKMSElement && (
        <div className={styles.parent_folder}>
          {currentFolder.parentKMSElement.icon && (
            <div className={styles.icon}>
              {currentFolder.parentKMSElement.icon}
            </div>
          )}
          <span className={styles.name} onClick={() => void loadParentFolder()}>
            {currentFolder.parentKMSElement.file_name?.replace(/(\..+)$/, "")}
          </span>
          <Icon name="chevronRight" size="normal" color="black" />
        </div>
      )}
      <div className={styles.current_folder}>
        {currentFolder?.icon && (
          <div className={styles.icon}>{currentFolder.icon}</div>
        )}
        <span
          className={`${styles.name} ${
            currentFolder?.parentKMSElement ? styles.selected : ""
          }`}
        >
          {currentFolder?.file_name?.replace(/(\..+)$/, "")}
        </span>
      </div>
    </div>
  );
};

export default FolderExplorerHeader;
