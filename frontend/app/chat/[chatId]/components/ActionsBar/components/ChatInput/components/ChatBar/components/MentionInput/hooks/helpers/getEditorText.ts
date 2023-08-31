import { MentionData } from "@draft-js-plugins/mention";
import { EditorState } from "draft-js";

export const getEditorText = (editorState: EditorState): string => {
  const mentions: string[] = [];
  const editorEntities = editorState.getCurrentContent().getAllEntities();

  editorEntities.forEach((entity) => {
    const entityData = entity?.getData() as { mention?: MentionData };
    if (entityData.mention !== undefined) {
      mentions.push(entityData.mention.name);
    }
  });

  let content = editorState.getCurrentContent().getPlainText();

  for (const mention of mentions) {
    content = content.replace(`@#${mention}`, "");
  }

  return content.trim();
};
