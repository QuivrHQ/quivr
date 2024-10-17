"use client";
import { Editor, Extension } from "@tiptap/core";
import Focus from "@tiptap/extension-focus";
import { Link } from "@tiptap/extension-link";
import { BubbleMenu, EditorContent, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";
import { useRef, useState } from "react";

import { useBrainMention } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ChatEditor/Editor/hooks/useBrainMention";

import styles from "./TextEditor.module.scss";
import { TextEditorSearchBar } from "./components/TextEditorSearchBar/TextEditorSearchBar";
import { Toolbar } from "./components/Toolbar/Toolbar";
import { AIHighlight } from "./extensions/AIHighlight";

import { QuivrButton } from "../ui/QuivrButton/QuivrButton";

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
  const [searchBarOpen, setSearchBarOpen] = useState(true);
  const searchEditorRef = useRef<Editor>(null);

  const FocusSearchBar = Extension.create().extend({
    addKeyboardShortcuts: () => {
      return {
        "Mod-f": ({ editor }) => {
          const selection = editor.state.doc.textBetween(
            editor.state.selection.from,
            editor.state.selection.to
          );

          if (selection) {
            editor.commands.setSelectionHighlight();
          }

          setSearchBarOpen(true);
          searchEditorRef.current
            ?.chain()
            .focus()
            .setContent(selection, undefined, { preserveWhitespace: true })
            .run();

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
        AIHighlight.configure({
          HTMLAttributes: {
            class: styles.ai_highlight,
          },
        }),
      ],
      content: defaultContent,
      immediatelyRender: false,
      autofocus: true,
    },
    [items.length]
  );

  const toggleSearchBar = () => {
    if (searchBarOpen) {
      setSearchBarOpen(false);
      editor?.commands.focus();
    } else {
      setSearchBarOpen(true);
      searchEditorRef.current?.commands.focus();
    }
  };

  if (!editor) {
    return <></>;
  }

  return (
    <div className={styles.main_container}>
      <div className={styles.editor_wrapper}>
        <Toolbar toggleSearchBar={toggleSearchBar} editor={editor} />
        <div>
          <BubbleMenu
            shouldShow={() => {
              return editor.isActive("aiHighlight", { type: "ai" });
            }}
            tippyOptions={{
              moveTransition: "transform 0.1s",
              placement: "bottom-start",
            }}
            className={styles.bubble_menu}
            editor={editor}
          >
            <QuivrButton
              onClick={() => {
                editor
                  .chain()
                  .extendMarkRange("aiHighlight")
                  .unsetHighlight()
                  .run();
              }}
              label="Accept"
              color="primary"
              iconName="check"
            />
            <QuivrButton
              onClick={() => {
                editor.commands.undo();
              }}
              label="Decline"
              color="dangerous"
              iconName="close"
            />
          </BubbleMenu>
        </div>

        <EditorContent className={styles.content_wrapper} editor={editor} />
      </div>
      <div
        className={`${styles.search_bar_wrapper} ${
          searchBarOpen ? styles.active : ""
        }`}
      >
        <TextEditorSearchBar ref={searchEditorRef} editor={editor} />
      </div>
    </div>
  );
};
