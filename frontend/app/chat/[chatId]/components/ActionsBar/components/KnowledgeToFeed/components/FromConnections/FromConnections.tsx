import { useEffect } from "react";

import { ConnectionCards } from "@/lib/components/ConnectionCards/ConnectionCards";
import TextButton from "@/lib/components/ui/TextButton/TextButton";

import { useFromConnectionsContext } from "./FromConnectionsProvider/hooks/useFromConnectionContext";

export const FromConnections = (): JSX.Element => {
  const {
    currentSyncElements,
    setCurrentSyncElements,
    currentProvider,
    setCurrentProvider,
  } = useFromConnectionsContext();

  useEffect(() => {
    console.info(currentSyncElements);
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
              setCurrentProvider(undefined);
            }}
            small={true}
          />
          <div>
            <div>Synchronize {currentProvider} </div>
            OR
            <div></div>
          </div>
        </div>
      )}
    </div>
  );
};
