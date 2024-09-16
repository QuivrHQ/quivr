"use client";
import Focus from "@tiptap/extension-focus";
import { Link } from "@tiptap/extension-link";
import { EditorContent, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";

import { useBrainMention } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ChatEditor/Editor/hooks/useBrainMention";

import styles from "./TextEditor.module.scss";
import { TextEditorSearchBar } from "./components/TextEditorSearchBar/TextEditorSearchBar";
import { Toolbar } from "./components/Toolbar/Toolbar";

const defaultContent = `
  <h1>My Note</h1>
  <p>
    This is a note with the help of which you can jot down ideas and store them in your brains.<br>
    Start by typing <code>@</code> to select a brain!
  </p>
`;

export const TextEditor = (): JSX.Element => {
  const { BrainMention, items } = useBrainMention();

  const editor = useEditor(
    {
      extensions: [
        StarterKit.configure({}),
        Focus.configure({
          className: styles.has_focus,
          mode: "shallowest",
        }),
        Link.configure({
          openOnClick: false,
        }),
        BrainMention,
      ],
      content: defaultContent,
      immediatelyRender: false,
      autofocus: true,
    },
    [items.length]
  );
  if (!editor) {
    return <></>;
  }

  return (
    <div className={styles.main_container}>
      <div className={styles.editor_wrapper}>
        <Toolbar editor={editor} />
        <EditorContent className={styles.content_wrapper} editor={editor} />
      </div>
      <div className={styles.search_bar_wrapper}>
        <TextEditorSearchBar editor={editor} />
      </div>
    </div>
  );
};
