"use client";

import { useEffect } from "react";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { transformConnectionLabel } from "@/lib/helpers/providers";

import styles from "./FolderExplorerHeader.module.scss";

import { useKnowledgeContext } from "../../../KnowledgeProvider/hooks/useKnowledgeContext";

const FolderExplorerHeader = (): JSX.Element => {
  const {
    currentFolder,
    setCurrentFolder,
    exploringQuivr,
    providerRootSelected,
  } = useKnowledgeContext();

  const loadParentFolder = () => {
    if (currentFolder?.parentKMSElement) {
      setCurrentFolder({
        ...currentFolder.parentKMSElement,
        parentKMSElement: currentFolder.parentKMSElement.parentKMSElement,
      });
    }
  };

  const loadQuivrRoot = () => {
    setCurrentFolder(undefined);
  };

  useEffect(() => {
    if (currentFolder) {
      console.log("Current folder:", currentFolder);
    }
  });

  return (
    <div className={styles.header_wrapper}>
      {exploringQuivr && !currentFolder?.parentKMSElement ? (
        <>
          <span
            className={`${styles.name} ${
              currentFolder ? styles.hoverable : ""
            }`}
            onClick={() => void loadQuivrRoot()}
          >
            Quivr
          </span>
          {currentFolder && (
            <Icon name="chevronRight" size="normal" color="black" />
          )}
        </>
      ) : providerRootSelected ? (
        <span className={styles.name}>
          {transformConnectionLabel(providerRootSelected.provider)}
        </span>
      ) : (
        currentFolder?.parentKMSElement && (
          <div className={styles.parent_folder}>
            <span
              className={styles.name}
              onClick={() => void loadParentFolder()}
            >
              {currentFolder.parentKMSElement.file_name?.replace(/(\..+)$/, "")}
            </span>
            <Icon name="chevronRight" size="normal" color="black" />
          </div>
        )
      )}
      <div className={styles.current_folder}>
        {currentFolder?.icon && (
          <div className={styles.icon}>{currentFolder.icon}</div>
        )}
        <span
          className={`${styles.name} ${
            currentFolder?.parentKMSElement || (exploringQuivr && currentFolder)
              ? styles.selected
              : ""
          }`}
        >
          {currentFolder?.file_name?.replace(/(\..+)$/, "")}
        </span>
      </div>
    </div>
  );
};

export default FolderExplorerHeader;
