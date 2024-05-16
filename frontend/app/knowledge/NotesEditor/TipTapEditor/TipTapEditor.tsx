import { EditorContent, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";
import { useEffect } from "react";

import { useNotesEditorContext } from "@/lib/context/NotesEditorProvider/hooks/useNotesEditorContext";

import styles from "./TipTapEditor.module.scss";

const TipTapEditor = (): JSX.Element => {
  const { content } = useNotesEditorContext();

  const editor = useEditor({
    extensions: [StarterKit],
    content,
  });

  useEffect(() => {
    if (editor) {
      editor.commands.setContent(content);
    }
  }, [content, editor]);

  return (
    <div className={styles.editor_wrapper}>
      <EditorContent editor={editor} />
    </div>
  );
};

export default TipTapEditor;
