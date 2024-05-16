import { Editor, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";
import { useState } from "react";

export const useEditorContent = (): {
  editor: Editor | null;
  updateContent: (newContent: string) => void;
} => {
  const [content, setContent] = useState("<p>Hello World! 🌎️</p>");

  const editor: Editor | null = useEditor({
    extensions: [StarterKit],
    content,
  });

  const updateContent = (newContent: string) => {
    setContent(newContent);
    if (editor) {
      editor.commands.setContent(newContent);
    }
  };

  return { editor, updateContent };
};
