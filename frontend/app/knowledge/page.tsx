"use client";

import PageHeader from "@/lib/components/PageHeader/PageHeader";

import styles from "./page.module.scss";

const Knowledge = (): JSX.Element => {
  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader iconName="knowledge" label="My Knowledge" buttons={[]} />
      </div>
    </div>
  );
};

export default Knowledge;
