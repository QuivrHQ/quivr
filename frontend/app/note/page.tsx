"use client";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";
import { Tiptap } from "@/lib/components/Tiptap";

import styles from "./page.module.scss";

const Note = (): JSX.Element => {
  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader iconName="pen" label="Notetaker" buttons={[]} />
        <Tiptap />
      </div>
    </div>
  );
};

export default Note;
