"use client";
import { Editor } from "@tiptap/core";
import { useCallback, useState } from "react";

import { Modal } from "@/lib/components/ui/Modal/Modal";

import styles from "./Toolbar.module.scss";

import { ToolbarButton } from "../ToolbarButton/ToolbarButton";

export const ToolbarSectionSeparator = (): JSX.Element => {
  return (
    <div
      role="separator"
      aria-orientation="vertical"
      className={styles.separator}
    ></div>
  );
};

type ToolbarProps = {
  editor: Editor;
};

export const Toolbar = ({ editor }: ToolbarProps): JSX.Element => {
  const [linkModalOpen, setLinkModalOpen] = useState(false);

  const setLink = useCallback(() => {
    const previousUrl = editor.getAttributes("link").href as string;
    const url = window.prompt("URL", previousUrl);

    // cancelled
    if (url === null) {
      return;
    }

    const editorChain = editor.chain().focus().extendMarkRange("link");

    url === ""
      ? editorChain.unsetLink().run()
      : editorChain.setLink({ href: url }).run();
  }, [editor]);

  return (
    <div className={styles.toolbar}>
      <ToolbarButton
        aria-label="Toggle bold"
        iconName="bold"
        active={editor.isActive("bold")}
        setActive={editor.chain().focus().toggleBold().run}
      />
      <ToolbarButton
        aria-label="Toggle italic"
        iconName="italic"
        active={editor.isActive("italic")}
        setActive={editor.chain().focus().toggleItalic().run}
      />
      <ToolbarButton
        aria-label="Toggle strike"
        iconName="strikethrough"
        active={editor.isActive("strike")}
        setActive={editor.chain().focus().toggleStrike().run}
      />
      <ToolbarButton
        aria-label="Toggle link"
        iconName="link"
        active={editor.isActive("link")}
        // onClick={() => setLinkModalOpen(true)}
        setActive={setLink}
      />
      <Modal
        title="Add link"
        desc=""
        isOpen={linkModalOpen}
        setOpen={setLinkModalOpen}
      >
        <div>Hello world</div>
      </Modal>
      <ToolbarSectionSeparator />
      <ToolbarButton
        aria-label="Toggle ordered list"
        iconName="orderedList"
        active={editor.isActive("orderedList")}
        setActive={editor.chain().focus().toggleOrderedList().run}
      />
      <ToolbarButton
        aria-label="Toggle unordered list"
        iconName="unorderedList"
        active={editor.isActive("bulletList")}
        setActive={editor.chain().focus().toggleBulletList().run}
      />
      <ToolbarSectionSeparator />
      <ToolbarButton
        aria-label="Toggle blockquote"
        iconName="blockquote"
        active={editor.isActive("blockquote")}
        setActive={editor.chain().focus().toggleBlockquote().run}
      />
      <ToolbarButton
        aria-label="Toggle code"
        iconName="code"
        active={editor.isActive("code")}
        setActive={editor.chain().focus().toggleCode().run}
      />
      <ToolbarButton
        aria-label="Toggle code block"
        iconName="codeblock"
        active={editor.isActive("codeBlock")}
        setActive={editor.chain().focus().toggleCodeBlock().run}
      />
      <ToolbarSectionSeparator />
      <ToolbarButton
        aria-label="Toggle heading 1"
        iconName="heading1"
        active={editor.isActive("heading", { level: 1 })}
        setActive={editor.chain().focus().toggleHeading({ level: 1 }).run}
      />
      <ToolbarButton
        aria-label="Toggle heading 2"
        iconName="heading2"
        active={editor.isActive("heading", { level: 2 })}
        setActive={editor.chain().focus().toggleHeading({ level: 2 }).run}
      />
      <ToolbarButton
        aria-label="Toggle heading 3"
        iconName="heading3"
        active={editor.isActive("heading", { level: 3 })}
        setActive={editor.chain().focus().toggleHeading({ level: 3 }).run}
      />
      <ToolbarButton
        aria-label="Toggle heading 4"
        iconName="heading4"
        active={editor.isActive("heading", { level: 4 })}
        setActive={editor.chain().focus().toggleHeading({ level: 4 }).run}
      />
      <ToolbarButton
        aria-label="Toggle heading 5"
        iconName="heading5"
        active={editor.isActive("heading", { level: 5 })}
        setActive={editor.chain().focus().toggleHeading({ level: 5 }).run}
      />
      <ToolbarButton
        aria-label="Toggle heading 6"
        iconName="heading6"
        active={editor.isActive("heading", { level: 6 })}
        setActive={editor.chain().focus().toggleHeading({ level: 6 }).run}
      />
    </div>
  );
};
