import Image from "next/image";
import { useEffect, useState } from "react";

import { Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";

import styles from "./FromConnections.module.scss";

export const FromConnections = (): JSX.Element => {
  const [userSyncs, setUserSyncs] = useState<Sync[]>([]);
  const { getSyncFiles, getUserSyncs, iconUrls } = useSync();

  useEffect(() => {
    void (async () => {
      try {
        const res: Sync[] = await getUserSyncs();
        setUserSyncs(res.filter((sync) => !!sync.credentials.token));
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  const handleClick = async (syncId: number) => {
    const res = await getSyncFiles(syncId);
    console.info(res);
  };

  return (
    <div className={styles.user_syncs_wrapper}>
      {userSyncs.map((sync, index) => (
        <div
          className={styles.user_sync_wrapper}
          key={index}
          onClick={() => void handleClick(sync.id)}
        >
          <Image
            src={iconUrls[sync.provider] || ""}
            alt={sync.name}
            width={24}
            height={24}
          />
          <div>{sync.name}</div>
        </div>
      ))}
    </div>
  );
};
