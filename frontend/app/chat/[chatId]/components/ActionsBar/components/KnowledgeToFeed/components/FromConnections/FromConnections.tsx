import { ConnectionCards } from "@/lib/components/ConnectionCards/ConnectionCards";

import { useFromConnections } from "./hooks/useFromConnections";

export const FromConnections = (): JSX.Element => {
  const { currentSyncElements } = useFromConnections();

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
