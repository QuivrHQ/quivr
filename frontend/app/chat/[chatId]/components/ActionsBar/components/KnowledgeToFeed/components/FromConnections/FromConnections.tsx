import { useEffect, useState } from "react";

import { SyncElement } from "@/lib/api/sync/types";
import { ConnectionCards } from "@/lib/components/ConnectionCards/ConnectionCards";
import SwitchButton from "@/lib/components/ui/SwitchButton/SwitchButton";
import TextButton from "@/lib/components/ui/TextButton/TextButton";

import { FileLine } from "./FileLine/FileLine";
import { FolderLine } from "./FolderLine/FolderLine";
import styles from "./FromConnections.module.scss";
import { useFromConnectionsContext } from "./FromConnectionsProvider/hooks/useFromConnectionContext";

export const FromConnections = (): JSX.Element => {
  const { currentSyncElements, setCurrentSyncElements } =
    useFromConnectionsContext();
  const [currentFiles, setCurrentFiles] = useState<SyncElement[]>([]);
  const [currentFolders, setCurrentFolders] = useState<SyncElement[]>([]);
  const [selectSpecificFiles, setselectSpecificFiles] =
    useState<boolean>(false);

  useEffect(() => {
    setCurrentFiles(
      currentSyncElements?.files.filter((file) => !file.is_folder) ?? []
    );
    setCurrentFolders(
      currentSyncElements?.files.filter((file) => file.is_folder) ?? []
    );
  }, [currentSyncElements]);

  return (
    <div>
      {!currentSyncElements?.files.length ? (
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
              <div key={folder.id}>
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
