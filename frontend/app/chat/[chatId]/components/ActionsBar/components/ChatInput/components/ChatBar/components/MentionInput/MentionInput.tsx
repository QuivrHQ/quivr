/* eslint-disable max-lines */
import Editor from "@draft-js-plugins/editor";
import { EditorState, getDefaultKeyBinding } from "draft-js";
import { ReactElement, useEffect } from "react";
import { useTranslation } from "react-i18next";

import "@draft-js-plugins/mention/lib/plugin.css";
import "draft-js/dist/Draft.css";

import { AddNewBrainButton } from "./components";
import { BrainSuggestion } from "./components/BrainSuggestion";
import { useMentionInput } from "./hooks/useMentionInput";

import { MentionTriggerType } from "@/app/chat/[chatId]/components/ActionsBar/types";
import { Popover } from "@radix-ui/react-popover";

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
    editorState,
    onOpenChange,
    onSearchChange,
    open,
    plugins,
    setEditorState,
    suggestions,
    onAddMention,
    mentionItems,
    insertMention,
  } = useMentionInput({
    message,
  });

  const { t } = useTranslation(["chat"]);

  type TriggerMap = {
    trigger: MentionTriggerType;
    content: string;
  };

  const resetEditorContent = () => {
    const currentMentions = getEditorCurrentMentions();
    let newEditorState = EditorState.createEmpty();
    currentMentions.forEach((mention) => {
      if (mention.trigger === "@") {
        const correspondingMention = mentionItems["@"].find(
          (item) => item.name === mention.content
        );
        if (correspondingMention !== undefined) {
          if (mention.trigger === "@") {
            newEditorState = insertMention(
              correspondingMention,
              mention.trigger,
              newEditorState
            );
          }
        }
      }
    });
    setEditorState(newEditorState);
  };

  const getEditorCurrentMentions = (): TriggerMap[] => {
    const contentState = editorState.getCurrentContent();
    const plainText = contentState.getPlainText();
    const mentionTriggers = Object.keys(mentionItems);

    const mentionTexts: TriggerMap[] = [];

    mentionTriggers.forEach((trigger) => {
      if (trigger === "@") {
        mentionItems["@"].forEach((item) => {
          const mentionText = `${trigger}${item.name}`;
          if (plainText.includes(mentionText)) {
            mentionTexts.push({
              trigger: trigger as MentionTriggerType,
              content: item.name,
            });
          }
        });
      }
    });
    return mentionTexts;
  };

  const keyBindingFn = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      onSubmit();
      return "submit";
    }

    return getDefaultKeyBinding(e);
  };

  const getNonMentionTexts = (editorCurrentState: EditorState): string => {
    const contentState = editorCurrentState.getCurrentContent();
    let plainText = contentState.getPlainText();
    Object.keys(mentionItems).forEach((trigger) => {
      if (trigger === "@") {
        mentionItems[trigger].forEach((item) => {
          const regex = new RegExp(`${trigger}${item.name}`, "g");
          plainText = plainText.replace(regex, "");
        });
      }
    });
    return plainText;
  };

  const handleEditorChange = (newEditorState: EditorState) => {
    setEditorState(newEditorState);
    const currentMessage = getNonMentionTexts(newEditorState);
    setMessage(currentMessage);
  };

  useEffect(() => {
    if (message === "") {
      resetEditorContent();
    }
  }, [message]);

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
            <Popover>
              <div className="z-50 bg-white dark:bg-black border border-black/10 dark:border-white/25 rounded-md shadow-md overflow-y-auto min-w-32">
                {children}
                <AddNewBrainButton />
              </div>
            </Popover>
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
