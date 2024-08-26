"use client";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";

import styles from "./page.module.scss";

const Note = (): JSX.Element => {
  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader iconName="pen" label="Notetaker" buttons={[]} />
      </div>
    </div>
  );
};

export default Note;
