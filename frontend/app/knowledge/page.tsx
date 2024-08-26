"use client";

import { useEffect } from "react";

import { Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import PageHeader from "@/lib/components/PageHeader/PageHeader";

import styles from "./page.module.scss";

const Knowledge = (): JSX.Element => {
  const { getUserSyncs } = useSync();

  const fetchUserSyncs = async () => {
    try {
      const res: Sync[] = await getUserSyncs();
      console.info(res);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    void fetchUserSyncs();
  }, []);

  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader iconName="knowledge" label="My Knowledge" buttons={[]} />
      </div>
    </div>
  );
};

export default Knowledge;
