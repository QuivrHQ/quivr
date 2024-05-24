import { useEffect, useState } from "react";

import { Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";

export const FromConnections = (): JSX.Element => {
  const [userSyncs, setUserSyncs] = useState<Sync[]>([]);
  const { getUserSyncs } = useSync();

  useEffect(() => {
    void (async () => {
      try {
        const res: Sync[] = await getUserSyncs();
        setUserSyncs(res);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  return (
    <div>
      {userSyncs.map((sync, index) => (
        <div key={index}>{sync.name}</div>
      ))}
    </div>
  );
};
