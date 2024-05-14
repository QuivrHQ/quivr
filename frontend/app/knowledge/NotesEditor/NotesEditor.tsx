"use client";

import styles from "./NotesEditor.module.scss";
import TipTapEditor from "./TipTapEditor/TipTapEditor";

const NotesEditor = (): JSX.Element => {
  return (
    <div className={styles.notes_editor_wrapper}>
      <TipTapEditor />
    </div>
  );
};

export default NotesEditor;
