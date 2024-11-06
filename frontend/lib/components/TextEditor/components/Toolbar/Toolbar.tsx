"use client";
import { Editor } from "@tiptap/core";
import { useState } from "react";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

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
  searchBarOpen: boolean;
  toggleSearchBar: () => void;
};

export const Toolbar = ({
  editor,
  searchBarOpen,
  toggleSearchBar,
}: ToolbarProps): JSX.Element => {
  const [linkModalOpen, setLinkModalOpen] = useState(false);
  const [urlInp, setUrlInp] = useState("");

  const setLink = () => {
    const editorChain = editor.chain().extendMarkRange("link").focus();

    urlInp === ""
      ? editorChain.unsetLink().run()
      : editorChain.setLink({ href: urlInp }).run();

    setLinkModalOpen(false);
  };

  const openLinkModal = () => {
    const prevUrl = editor.getAttributes("link").href as string;
    setUrlInp(prevUrl || "");
    setLinkModalOpen(true);
  };

  return (
    <div className={styles.toolbar}>
      <ToolbarButton
        aria-label="Toggle bold"
        iconName="bold"
        active={editor.isActive("bold")}
        setActive={() => editor.chain().toggleBold().focus().run()}
      />
      <ToolbarButton
        aria-label="Toggle italic"
        iconName="italic"
        active={editor.isActive("italic")}
        setActive={() => editor.chain().toggleItalic().focus().run()}
      />
      <ToolbarButton
        aria-label="Toggle strike"
        iconName="strikethrough"
        active={editor.isActive("strike")}
        setActive={() => editor.chain().toggleStrike().focus().run()}
      />
      <ToolbarButton
        aria-label="Toggle link"
        iconName="link"
        active={editor.isActive("link")}
        onClick={openLinkModal}
      />
      <Modal
        title="Add link"
        desc=""
        size="auto"
        isOpen={linkModalOpen}
        setOpen={setLinkModalOpen}
        CloseTrigger={
          <div className={styles.modal_close_trigger_wrapper}>
            <Button variant={"danger"}>Cancel</Button>
            <Button onClick={() => setLink()}>Done</Button>
          </div>
        }
      >
        <TextInput
          inputValue={urlInp}
          label="Url"
          onSubmit={setLink}
          setInputValue={setUrlInp}
        />
      </Modal>
      <ToolbarSectionSeparator />
      <ToolbarButton
        aria-label="Toggle ordered list"
        iconName="orderedList"
        active={editor.isActive("orderedList")}
        setActive={() => editor.chain().toggleOrderedList().focus().run()}
      />
      <ToolbarButton
        aria-label="Toggle unordered list"
        iconName="unorderedList"
        active={editor.isActive("bulletList")}
        setActive={() => editor.chain().toggleBulletList().focus().run()}
      />
      <ToolbarSectionSeparator />
      <ToolbarButton
        aria-label="Toggle blockquote"
        iconName="blockquote"
        active={editor.isActive("blockquote")}
        setActive={() => editor.chain().toggleBlockquote().focus().run()}
      />
      <ToolbarButton
        aria-label="Toggle code"
        iconName="code"
        active={editor.isActive("code")}
        setActive={() => editor.chain().toggleCode().focus().run()}
      />
      <ToolbarButton
        aria-label="Toggle code block"
        iconName="codeblock"
        active={editor.isActive("codeBlock")}
        setActive={() => editor.chain().toggleCodeBlock().focus().run()}
      />
      <ToolbarSectionSeparator />
      <ToolbarButton
        aria-label="Toggle heading 1"
        iconName="heading1"
        active={editor.isActive("heading", { level: 1 })}
        setActive={() =>
          editor.chain().toggleHeading({ level: 1 }).focus().run()
        }
      />
      <ToolbarButton
        aria-label="Toggle heading 2"
        iconName="heading2"
        active={editor.isActive("heading", { level: 2 })}
        setActive={() =>
          editor.chain().toggleHeading({ level: 2 }).focus().run()
        }
      />
      <ToolbarButton
        aria-label="Toggle heading 3"
        iconName="heading3"
        active={editor.isActive("heading", { level: 3 })}
        setActive={() =>
          editor.chain().toggleHeading({ level: 3 }).focus().run()
        }
      />
      <ToolbarButton
        aria-label="Toggle heading 4"
        iconName="heading4"
        active={editor.isActive("heading", { level: 4 })}
        setActive={() =>
          editor.chain().toggleHeading({ level: 4 }).focus().run()
        }
      />
      <ToolbarButton
        aria-label="Toggle heading 5"
        iconName="heading5"
        active={editor.isActive("heading", { level: 5 })}
        setActive={() =>
          editor.chain().toggleHeading({ level: 5 }).focus().run()
        }
      />
      <ToolbarButton
        aria-label="Toggle heading 6"
        iconName="heading6"
        active={editor.isActive("heading", { level: 6 })}
        setActive={() =>
          editor.chain().toggleHeading({ level: 6 }).focus().run()
        }
      />

      <div className={styles.focusSearchBarBtn}>
        <QuivrButton
          onClick={toggleSearchBar}
          label={searchBarOpen ? "Close Search Bar" : "Ask Brain"}
          color="primary"
          iconName={"chat"}
        />
      </div>
    </div>
  );
};
