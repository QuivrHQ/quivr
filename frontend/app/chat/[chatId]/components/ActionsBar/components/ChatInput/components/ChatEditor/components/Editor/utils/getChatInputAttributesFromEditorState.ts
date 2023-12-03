import { Editor } from "@tiptap/core";

type ChatInputAttributes = {
  text: string;
  promptId: string;
  brainId: string;
};

export const getChatInputAttributesFromEditorState = (
  editor: Editor | null
): ChatInputAttributes => {
  if (editor === null) {
    return {
      text: "",
      promptId: "",
      brainId: "",
    };
  }

  const editorJsonContent = editor.getJSON();

  if (
    editorJsonContent.content === undefined ||
    editorJsonContent.content.length === 0
  ) {
    return {
      text: "",
      promptId: "",
      brainId: "",
    };
  }

  let text = "";
  let prompt = "";
  let brain = "";

  editorJsonContent.content.forEach((block) => {
    if (block.content === undefined || block.content.length === 0) {
      return;
    }

    block.content.forEach((innerBlock) => {
      if (innerBlock.type === "text") {
        text += innerBlock.text;
      }
      if (innerBlock.type === "mention#") {
        prompt = (innerBlock.attrs?.id as string | undefined) ?? "";
      }
      if (innerBlock.type === "mention@") {
        brain = (innerBlock.attrs?.id as string | undefined) ?? "";
      }
    });
  });

  return {
    text,
    promptId: prompt,
    brainId: brain,
  };
};
