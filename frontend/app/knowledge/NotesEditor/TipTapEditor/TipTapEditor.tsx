import { TextAlign } from "@tiptap/extension-text-align";
import { EditorContent, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";
import { useEffect } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import { useNotesEditorContext } from "@/lib/context/NotesEditorProvider/hooks/useNotesEditorContext";

import styles from "./TipTapEditor.module.scss";

import "@/app/globals.css";

const TipTapEditor = (): JSX.Element => {
  const { content, expand, setExpand } = useNotesEditorContext();

  const tipTapEditor = useEditor({
    extensions: [
      StarterKit,
      TextAlign.configure({
        types: ["heading", "paragraph"],
      }),
    ],
    parseOptions: {
      preserveWhitespace: "full",
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
        <div className={styles.text_manipulation_wrapper}>
          <Icon
            name="justifyLeft"
            size="large"
            color={
              tipTapEditor?.isActive({ textAlign: "left" })
                ? "primary"
                : "black"
            }
            handleHover={true}
            onClick={() =>
              void tipTapEditor?.chain().focus().setTextAlign("left").run()
            }
          />
          <Icon
            name="justifyCenter"
            size="large"
            color={
              tipTapEditor?.isActive({ textAlign: "center" })
                ? "primary"
                : "black"
            }
            handleHover={true}
            onClick={() =>
              void tipTapEditor?.chain().focus().setTextAlign("center").run()
            }
          />
          <Icon
            name="justifyRight"
            size="large"
            color={
              tipTapEditor?.isActive({ textAlign: "right" })
                ? "primary"
                : "black"
            }
            handleHover={true}
            onClick={() =>
              void tipTapEditor?.chain().focus().setTextAlign("right").run()
            }
          />
        </div>
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
