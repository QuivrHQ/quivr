import { MentionData } from "@draft-js-plugins/mention";
import { EditorState } from "draft-js";

import { isMention } from "./isMention";

export const getEditorMentions = (editorState: EditorState): MentionData[] => {
  const contentState = editorState.getCurrentContent();
  const entities = contentState.getAllEntities();

  const mentions: MentionData[] = [];

  entities.forEach((contentBlock) => {
    if (isMention(contentBlock?.getType())) {
      mentions.push(
        (contentBlock?.getData() as { mention: MentionData }).mention
      );
    }
  });

  return mentions;
};
