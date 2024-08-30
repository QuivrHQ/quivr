"use client";
import { Editor } from "@tiptap/core";
import { useState } from "react";

import { Modal } from "@/lib/components/ui/Modal/Modal";

import styles from "./Toolbar.module.scss";

import { ToolbarButton } from "../ToolbarButton";

type Props = {
  editor: Editor;
};

export const Toolbar = ({ editor }: Props): JSX.Element => {
  const [linkModalOpen, setLinkModalOpen] = useState(false);

  //   const setLink = useCallback(() => {
  //     const previousUrl = editor.getAttributes("link").href as string;
  //     // const url = window.prompt("URL", previousUrl);
  //     const url = null;

  //     // cancelled
  //     if (url === null) {
  //       return;
  //     }

  //     // empty
  //     if (url === "") {
  //       editor.chain().focus().extendMarkRange("link").unsetLink().run();

  //       return;
  //     }

  //     // update link
  //     editor.chain().focus().extendMarkRange("link").setLink({ href: url }).run();
  //   }, [editor]);

  return (
    <div className={styles.toolbar}>
      <ToolbarButton
        iconName="bold"
        active={editor.isActive("bold")}
        setActive={editor.chain().focus().toggleBold().run}
      />
      <ToolbarButton
        iconName="italic"
        active={editor.isActive("italic")}
        setActive={editor.chain().focus().toggleItalic().run}
      />
      <ToolbarButton
        iconName="strikethrough"
        active={editor.isActive("strike")}
        setActive={editor.chain().focus().toggleStrike().run}
      />
      <ToolbarButton
        iconName="link"
        active={editor.isActive("link")}
        // onClick={() => setLinkModalOpen(true)}
        // setActive={editor.chain().focus().toggleStrike().run}
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
        iconName="orderedList"
        active={editor.isActive("orderedList")}
        setActive={editor.chain().focus().toggleOrderedList().run}
      />

      <ToolbarButton
        iconName="unorderedList"
        active={editor.isActive("bulletList")}
        setActive={editor.chain().focus().toggleBulletList().run}
      />

      <ToolbarSectionSeparator />

      <ToolbarButton
        iconName="blockquote"
        active={editor.isActive("blockquote")}
        setActive={editor.chain().focus().toggleBlockquote().run}
      />

      <ToolbarButton
        iconName="code"
        active={editor.isActive("code")}
        setActive={editor.chain().focus().toggleCode().run}
      />

      <ToolbarButton
        iconName="codeblock"
        active={editor.isActive("codeBlock")}
        setActive={editor.chain().focus().toggleCodeBlock().run}
      />

      <ToolbarSectionSeparator />

      <ToolbarButton
        iconName="heading1"
        active={editor.isActive("heading", { level: 1 })}
        setActive={editor.chain().focus().toggleHeading({ level: 1 }).run}
      />
      <ToolbarButton
        iconName="heading2"
        active={editor.isActive("heading", { level: 2 })}
        setActive={editor.chain().focus().toggleHeading({ level: 2 }).run}
      />
      <ToolbarButton
        iconName="heading3"
        active={editor.isActive("heading", { level: 3 })}
        setActive={editor.chain().focus().toggleHeading({ level: 3 }).run}
      />
      <ToolbarButton
        iconName="heading4"
        active={editor.isActive("heading", { level: 4 })}
        setActive={editor.chain().focus().toggleHeading({ level: 4 }).run}
      />
      <ToolbarButton
        iconName="heading5"
        active={editor.isActive("heading", { level: 5 })}
        setActive={editor.chain().focus().toggleHeading({ level: 5 }).run}
      />
      <ToolbarButton
        iconName="heading6"
        active={editor.isActive("heading", { level: 6 })}
        setActive={editor.chain().focus().toggleHeading({ level: 6 }).run}
      />
    </div>
  );
};

export const ToolbarSectionSeparator = (): JSX.Element => {
  return <div aria-hidden className={styles.separator}></div>;
};
