import { EditorContent, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";
import { useEffect } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import { useNotesEditorContext } from "@/lib/context/NotesEditorProvider/hooks/useNotesEditorContext";

import styles from "./TipTapEditor.module.scss";

import "@/app/globals.css";

const TipTapEditor = (): JSX.Element => {
  const { content, updateContent, expand, setExpand } = useNotesEditorContext();

  const tipTapEditor = useEditor({
    extensions: [StarterKit],
    parseOptions: {
      preserveWhitespace: "full",
    },
    onUpdate: ({ editor }) => {
      updateContent(editor.getHTML());
    },
  });

  useEffect(() => {
    if (tipTapEditor) {
      tipTapEditor.commands.setContent(content);
    }
  }, [content, tipTapEditor]);

  return (
    <div className={styles.editor_wrapper}>
      <div className={styles.editor_header}>
        <Icon
          name={expand ? "collapse" : "expand"}
          size="normal"
          color="black"
          handleHover={true}
          onClick={() => setExpand(!expand)}
        />
      </div>
      <EditorContent editor={tipTapEditor} />
    </div>
  );
};

export default TipTapEditor;
