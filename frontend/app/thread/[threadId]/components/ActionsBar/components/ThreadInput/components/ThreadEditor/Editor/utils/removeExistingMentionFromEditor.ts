import { Editor, JSONContent } from "@tiptap/core";

export const removeExistingMentionFromEditor = (
  editor: Editor,
  mentionName: string
): void => {
  let newContent = editor.state.doc.toJSON() as JSONContent | undefined;

  if (newContent?.content !== undefined) {
    let mentionRemoved = false;

    const filteredContent = newContent.content.map((contentItem) => {
      if (contentItem.content) {
        const filtered = contentItem.content.filter((node) => {
          if (!mentionRemoved && node.type === mentionName) {
            mentionRemoved = true;

            return false;
          }

          return true;
        });

        return { ...contentItem, content: filtered };
      }

      return contentItem;
    });

    newContent = { ...newContent, content: filteredContent };
    editor.commands.setContent(newContent);
  }
};
