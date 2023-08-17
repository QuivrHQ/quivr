import Editor from "@draft-js-plugins/editor";
import { Popover } from "@draft-js-plugins/mention";
import { ReactElement } from "react";
import { useTranslation } from "react-i18next";

import "draft-js/dist/Draft.css";
import { AddNewBrainButton } from "./components/AddNewBrainButton";
import { useMentionInput } from "./hooks/useMentionInput";

export const CustomComponentMentionEditor = (): ReactElement => {
  const {
    mentionInputRef,
    MentionSuggestions,
    editorState,
    onOpenChange,
    onSearchChange,
    open,
    plugins,
    setEditorState,
    suggestions,
    onAddMention,
  } = useMentionInput();
  const { t } = useTranslation(["chat"]);

  return (
    <div
      className="w-full"
      onClick={() => {
        mentionInputRef.current?.focus();
      }}
    >
      <Editor
        editorKey={"editor"}
        editorState={editorState}
        onChange={setEditorState}
        plugins={plugins}
        ref={mentionInputRef}
        placeholder={t("actions_bar_placeholder")}
      />
      <MentionSuggestions
        open={open}
        onOpenChange={onOpenChange}
        suggestions={suggestions}
        onSearchChange={onSearchChange}
        popoverContainer={({ children, ...otherProps }) => (
          <Popover {...otherProps}>
            <div className="z-50 bg-white dark:bg-black border border-black/10 dark:border-white/25 rounded-md shadow-md overflow-y-auto">
              {children}
              <AddNewBrainButton />
            </div>
          </Popover>
        )}
        onAddMention={onAddMention}
        entryComponent={({ mention, ...otherProps }) => (
          <p
            {...otherProps}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer"
          >
            {mention.name}
          </p>
        )}
      />
    </div>
  );
};
