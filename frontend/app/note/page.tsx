"use client";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";
import { TextEditor } from "@/lib/components/TextEditor/TextEditor";

import styles from "./page.module.scss";

const NotetakerPage = (): JSX.Element => {
  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader iconName="pen" label="Notetaker" buttons={[]} />
      </div>
      <div className={styles.note_page_container}>
        <TextEditor />
      </div>
    </div>
  );
};

export default NotetakerPage;
