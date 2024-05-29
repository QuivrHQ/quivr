import { useEffect } from "react";

import { ConnectionCards } from "@/lib/components/ConnectionCards/ConnectionCards";

import { useFromConnectionsContext } from "./FromConnectionsProvider/hooks/useFromConnectionContext";

export const FromConnections = (): JSX.Element => {
  const { currentSyncElements } = useFromConnectionsContext();

  useEffect(() => {
    console.info(currentSyncElements);
  }, [currentSyncElements]);

  return (
    <div>
      {!currentSyncElements?.files.length ? (
        <ConnectionCards fromAddKnowledge={true} />
      ) : (
        <div>{currentSyncElements.files.length}</div>
      )}
    </div>
  );
};
