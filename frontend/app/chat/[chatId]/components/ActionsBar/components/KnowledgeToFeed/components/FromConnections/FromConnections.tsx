import { useEffect, useState } from "react";

import { SyncElement } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { ConnectionCards } from "@/lib/components/ConnectionCards/ConnectionCards";
import SwitchButton from "@/lib/components/ui/SwitchButton/SwitchButton";
import TextButton from "@/lib/components/ui/TextButton/TextButton";

import { FileLine } from "./FileLine/FileLine";
import { FolderLine } from "./FolderLine/FolderLine";
import styles from "./FromConnections.module.scss";
import { useFromConnectionsContext } from "./FromConnectionsProvider/hooks/useFromConnectionContext";

export const FromConnections = (): JSX.Element => {
  const { currentSyncElements, setCurrentSyncElements, currentSyncId } =
    useFromConnectionsContext();
  const [currentFiles, setCurrentFiles] = useState<SyncElement[]>([]);
  const [currentFolders, setCurrentFolders] = useState<SyncElement[]>([]);
  const [selectSpecificFiles, setselectSpecificFiles] =
    useState<boolean>(false);
  const { getSyncFiles } = useSync();

  useEffect(() => {
    setCurrentFiles(
      currentSyncElements?.files.filter((file) => !file.is_folder) ?? []
    );
    setCurrentFolders(
      currentSyncElements?.files.filter((file) => file.is_folder) ?? []
    );
  }, [currentSyncElements]);

  const handleGetSyncFiles = async (userSyncId: number, folderId: string) => {
    try {
      const res = await getSyncFiles(userSyncId, folderId);
      setCurrentSyncElements(res);
      console.info(res);
    } catch (error) {
      console.error("Failed to get sync files:", error);
    }
  };

  return (
    <div>
      {!currentSyncElements?.files.length || !currentSyncId ? (
        <ConnectionCards fromAddKnowledge={true} />
      ) : (
        <div className={styles.from_connection_wrapper}>
          <div className={styles.header_buttons}>
            <TextButton
              label="Back"
              iconName="chevronLeft"
              color="black"
              onClick={() => {
                setCurrentSyncElements({ files: [] });
              }}
              small={true}
            />
            <SwitchButton
              label="Select specific files"
              checked={selectSpecificFiles}
              setChecked={setselectSpecificFiles}
            />
          </div>
          <div className={styles.connection_content}>
            {currentFolders.map((folder) => (
              <div
                key={folder.id}
                onClick={() => {
                  void handleGetSyncFiles(currentSyncId, folder.id);
                }}
              >
                <FolderLine name={folder.name} />
              </div>
            ))}
            {currentFiles.map((file) => (
              <div key={file.id}>
                <FileLine name={file.name} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
