import { useEffect, useState } from "react";

import { SyncElement } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { ConnectionCards } from "@/lib/components/ConnectionCards/ConnectionCards";
import TextButton from "@/lib/components/ui/TextButton/TextButton";
import { useUserData } from "@/lib/hooks/useUserData";

import { FileLine } from "./FileLine/FileLine";
import { FolderLine } from "./FolderLine/FolderLine";
import styles from "./FromConnections.module.scss";
import { useFromConnectionsContext } from "./FromConnectionsProvider/hooks/useFromConnectionContext";

export const FromConnections = (): JSX.Element => {
  const [folderStack, setFolderStack] = useState<(string | null)[]>([]);
  const { currentSyncElements, setCurrentSyncElements, currentSyncId } =
    useFromConnectionsContext();
  const [currentFiles, setCurrentFiles] = useState<SyncElement[]>([]);
  const [currentFolders, setCurrentFolders] = useState<SyncElement[]>([]);
  const { getSyncFiles } = useSync();
  const { userData } = useUserData();

  const isPremium = userData?.is_premium;

  useEffect(() => {
    setCurrentFiles(
      currentSyncElements?.files.filter((file) => !file.is_folder) ?? []
    );
    setCurrentFolders(
      currentSyncElements?.files.filter((file) => file.is_folder) ?? []
    );
  }, [currentSyncElements]);

  const handleGetSyncFiles = async (
    userSyncId: number,
    folderId: string | null
  ) => {
    try {
      let res;
      if (folderId !== null) {
        res = await getSyncFiles(userSyncId, folderId);
      } else {
        res = await getSyncFiles(userSyncId);
      }
      setCurrentSyncElements(res);
    } catch (error) {
      console.error("Failed to get sync files:", error);
    }
  };

  const handleBackClick = async () => {
    if (folderStack.length > 0 && currentSyncId) {
      const newFolderStack = [...folderStack];
      newFolderStack.pop();
      setFolderStack(newFolderStack);
      const parentFolderId = newFolderStack[newFolderStack.length - 1];
      await handleGetSyncFiles(currentSyncId, parentFolderId);
    } else {
      setCurrentSyncElements({ files: [] });
    }
  };

  const handleFolderClick = async (userSyncId: number, folderId: string) => {
    setFolderStack([...folderStack, folderId]);
    await handleGetSyncFiles(userSyncId, folderId);
  };

  return (
    <div className={styles.from_connection_container}>
      {!currentSyncId ? (
        <ConnectionCards fromAddKnowledge={true} />
      ) : (
        <div className={styles.from_connection_wrapper}>
          <div className={styles.header_buttons}>
            <TextButton
              label="Back"
              iconName="chevronLeft"
              color="black"
              onClick={() => {
                void handleBackClick();
              }}
              small={true}
              disabled={!folderStack.length}
            />
          </div>
          <div className={styles.connection_content}>
            {currentFolders.map((folder) => (
              <div
                key={folder.id}
                onClick={() => {
                  void handleFolderClick(currentSyncId, folder.id);
                }}
              >
                <FolderLine
                  name={folder.name ?? ""}
                  selectable={!!isPremium}
                  id={folder.id}
                />
              </div>
            ))}
            {currentFiles.map((file) => (
              <div key={file.id}>
                <FileLine
                  name={file.name ?? ""}
                  selectable={true}
                  id={file.id}
                />
              </div>
            ))}
            {!currentFiles.length && !currentFolders.length && (
              <span className={styles.empty_folder}>Empty folder</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
