"use client";

import { EditorContent, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";

import styles from "./TipTapEditor.module.scss";

const TipTapEditor = (): JSX.Element => {
  const editor = useEditor({
    extensions: [StarterKit],
    content: "<p>Hello World! 🌎️</p>",
  });

  return (
    <div className={styles.editor_wrapper}>
      <EditorContent editor={editor} />
    </div>
  );
};

export default TipTapEditor;
