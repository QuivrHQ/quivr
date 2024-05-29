import { useEffect, useState } from "react";

import { SyncElement } from "@/lib/api/sync/types";
import { ConnectionCards } from "@/lib/components/ConnectionCards/ConnectionCards";
import TextButton from "@/lib/components/ui/TextButton/TextButton";

import { useFromConnectionsContext } from "./FromConnectionsProvider/hooks/useFromConnectionContext";

export const FromConnections = (): JSX.Element => {
  const { currentSyncElements, setCurrentSyncElements } =
    useFromConnectionsContext();
  const [currentFiles, setCurrentFiles] = useState<SyncElement[]>([]);
  const [currentFolders, setCurrentFolders] = useState<SyncElement[]>([]);

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
        <div>
          <TextButton
            label="Back to connections"
            iconName="chevronLeft"
            color="black"
            onClick={() => {
              setCurrentSyncElements({ files: [] });
            }}
            small={true}
          />
          <div>
            {currentFolders.map((folder) => (
              <div key={folder.id}>{folder.name}</div>
            ))}
            {currentFiles.map((file) => (
              <div key={file.id}>{file.name}</div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
