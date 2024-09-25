"use client";
import { Editor, Extension } from "@tiptap/core";
import Focus from "@tiptap/extension-focus";
import { Link } from "@tiptap/extension-link";
import { EditorContent, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";
import { useRef } from "react";

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
  <p>
    Also, you can press <code>Ctrl+F</code> or <code>Cmd+F</code> to ask a brain to generate some content for you! 
  </p>
`;

export const TextEditor = (): JSX.Element => {
  const { BrainMention, items } = useBrainMention();
  const searchEditorRef = useRef<Editor>(null);

  const FocusSearchBar = Extension.create().extend({
    addKeyboardShortcuts: () => {
      return {
        "Mod-f": () => {
          searchEditorRef.current?.commands.focus();

          return true;
        },
      };
    },
  });

  const editor = useEditor(
    {
      extensions: [
        StarterKit,
        Focus.configure({
          className: styles.has_focus,
          mode: "shallowest",
        }),
        Link.configure({
          openOnClick: false,
        }),
        BrainMention,
        FocusSearchBar,
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
        <Toolbar searchBarEditor={searchEditorRef.current} editor={editor} />
        <EditorContent className={styles.content_wrapper} editor={editor} />
      </div>
      <div className={styles.search_bar_wrapper}>
        <TextEditorSearchBar ref={searchEditorRef} editor={editor} />
      </div>
    </div>
  );
};
