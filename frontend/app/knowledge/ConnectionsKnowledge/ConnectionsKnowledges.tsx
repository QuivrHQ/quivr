"use client";

import { useEffect, useState } from "react";

import { Provider, Sync, SyncsByProvider } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";

import styles from "./ConnectionsKnowledge.module.scss";

const ConnectionsKnowledges = (): JSX.Element => {
  const [syncsByProvider, setSyncsByProvider] = useState<SyncsByProvider[]>([]);
  const { getUserSyncs } = useSync();

  const fetchUserSyncs = async () => {
    try {
      const res: Sync[] = await getUserSyncs();
      const groupedByProvider: { [key: string]: Sync[] } = {};

      res.forEach((sync) => {
        if (!groupedByProvider[sync.provider]) {
          groupedByProvider[sync.provider] = [];
        }
        groupedByProvider[sync.provider].push(sync);
      });

      const syncsByProviderArray: SyncsByProvider[] = Object.keys(
        groupedByProvider
      ).map((provider) => ({
        provider: provider as Provider,
        syncs: groupedByProvider[provider],
      }));

      setSyncsByProvider(syncsByProviderArray);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    void fetchUserSyncs();
  }, []);

  return (
    <div className={styles.connections_knowledge_container}>
      {syncsByProvider.map((providerGroup) => (
        <div key={providerGroup.provider}>
          <h3>{providerGroup.provider}</h3>
          <ul>
            {providerGroup.syncs.map((sync) => (
              <li key={sync.id}>{sync.name}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default ConnectionsKnowledges;
