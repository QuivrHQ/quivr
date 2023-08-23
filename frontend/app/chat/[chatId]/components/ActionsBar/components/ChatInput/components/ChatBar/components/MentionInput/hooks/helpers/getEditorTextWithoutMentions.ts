import { EditorState } from "draft-js";

import { MentionTriggerType } from "@/app/chat/[chatId]/components/ActionsBar/types";

import { getEditorMentions } from "./getEditorMentions";

export const getEditorTextWithoutMentions = (
  editorState: EditorState
): string => {
  const editorMentions = getEditorMentions(editorState);
  console.log({ editorMentions });
  const contentState = editorState.getCurrentContent();
  let plainText = contentState.getPlainText();
  editorMentions.forEach((editorMention) => {
    plainText = plainText.replace(
      `${editorMention.trigger as MentionTriggerType}${editorMention.name}`,
      ""
    );
  });

  return plainText.trim();
};
