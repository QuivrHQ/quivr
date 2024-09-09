"use client";

import PageHeader from "@/lib/components/PageHeader/PageHeader";

import ConnectionsKnowledges from "./ConnectionsKnowledge/ConnectionsKnowledges";
import styles from "./page.module.scss";

const Knowledge = (): JSX.Element => {
  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader iconName="knowledge" label="My Knowledge" buttons={[]} />
      </div>
      <div className={styles.content_wrapper}>
        <div className={styles.section}>
          <ConnectionsKnowledges />
        </div>
      </div>
    </div>
  );
};

export default Knowledge;
