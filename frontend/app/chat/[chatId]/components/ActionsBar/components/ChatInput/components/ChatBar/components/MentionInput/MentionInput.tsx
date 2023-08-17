import Editor from "@draft-js-plugins/editor";
import { Popover } from "@draft-js-plugins/mention";
import { EditorState, getDefaultKeyBinding } from "draft-js";
import { ReactElement } from "react";
import { useTranslation } from "react-i18next";

import "draft-js/dist/Draft.css";

import { AddNewBrainButton } from "./components/AddNewBrainButton";
import { BrainSuggestion } from "./components/BrainSuggestion";
import { useMentionInput } from "./hooks/useMentionInput";

type MentionInputProps = {
  onSubmit: (text?: string) => void;
};
export const MentionInput = ({ onSubmit }: MentionInputProps): ReactElement => {
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

  const keyBindingFn = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      const contentState = editorState.getCurrentContent();
      const rawText = contentState.getPlainText();
      onSubmit(rawText);
      // empty the editor content by keep
      setEditorState(EditorState.createEmpty());

      return "submit";
    }

    return getDefaultKeyBinding(e);
  };

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
        keyBindingFn={keyBindingFn}
      />
      <MentionSuggestions
        open={open}
        onOpenChange={onOpenChange}
        suggestions={suggestions}
        onSearchChange={onSearchChange}
        popoverContainer={({ children, ...otherProps }) => (
          <Popover {...otherProps}>
            <div className="z-50 bg-white dark:bg-black border border-black/10 dark:border-white/25 rounded-md shadow-md overflow-y-auto min-w-50">
              {children}
              <AddNewBrainButton />
            </div>
          </Popover>
        )}
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
