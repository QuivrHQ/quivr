import Editor from "@draft-js-plugins/editor";
import { ReactElement } from "react";
import { useTranslation } from "react-i18next";

import "@draft-js-plugins/mention/lib/plugin.css";
import "draft-js/dist/Draft.css";

import { AddNewBrainButton } from "./components";
import { BrainSuggestion } from "./components/BrainSuggestion";
import { useMentionInput } from "./hooks/useMentionInput";

type MentionInputProps = {
  onSubmit: () => void;
  setMessage: (text: string) => void;
  message: string;
};
export const MentionInput = ({
  onSubmit,
  setMessage,
  message,
}: MentionInputProps): ReactElement => {
  const {
    mentionInputRef,
    MentionSuggestions,
    keyBindingFn,
    editorState,
    onOpenChange,
    onSearchChange,
    open,
    plugins,
    suggestions,
    onAddMention,
    handleEditorChange,
  } = useMentionInput({
    message,
    onSubmit,
    setMessage,
  });

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
        onChange={handleEditorChange}
        plugins={plugins}
        ref={mentionInputRef}
        placeholder={t("actions_bar_placeholder")}
        keyBindingFn={keyBindingFn}
      />
      <MentionSuggestions
        open={open}
        onOpenChange={onOpenChange}
        suggestions={suggestions}
        onSearchChange={onSearchChange}
        popoverContainer={({ children }) => {
          return (
            <div className="z-50 bg-white dark:bg-black border border-black/10 dark:border-white/25 rounded-md shadow-md overflow-y-auto min-w-32">
              {children}
              <AddNewBrainButton />
            </div>
          );
        }}
        onAddMention={onAddMention}
        entryComponent={({ mention, ...otherProps }) => (
          <div {...otherProps}>
            <BrainSuggestion id={mention.id as string} content={mention.name} />
          </div>
        )}
      />
    </div>
  );
};
