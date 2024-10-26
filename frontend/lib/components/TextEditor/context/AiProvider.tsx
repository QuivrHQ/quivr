import { Editor, Range } from "@tiptap/core";
import { createContext, useState } from "react";

import { AIHighlightType } from "../extensions/types";

export type AiContextType = {
  range: Range | null;
  content: string;
  type: AIHighlightType;
  setAiContextAndHighlightRange: (range: Range, editor: Editor) => void;
  updateContent: (newContent: string, editor: Editor) => void;
  clearHighlight: (editor: Editor) => void;
  undo: (editor: Editor) => void;
};

export const AiContext = createContext<AiContextType | null>(null);

const AiProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [range, setRange] = useState<Range | null>(null);
  const [content, setContent] = useState("");
  const [prevContent, setPrevContent] = useState("");
  const [type, setType] = useState<AIHighlightType>("selection");

  const setAiContextAndHighlightRange = (
    newRange: Range,
    editor: Editor,
    newType: AIHighlightType = "selection"
  ) => {
    setRange(newRange);
    setPrevContent(content);
    setContent(editor.state.doc.textBetween(newRange.from, newRange.to));
    setType(newType);
    editor
      .chain()
      .unsetSelectionsInDocument()
      .setTextSelection(newRange)
      .setHighlight({ type: newType })
      .focus(newRange.to)
      .run();
  };

  const updateContent = (newContent: string, editor: Editor) => {
    if (range === null) {
      return;
    }
    editor.chain().deleteRange(range).insertContent(newContent).run();
    const finalPos = range.from + newContent.length;
    setAiContextAndHighlightRange(
      { from: range.from, to: finalPos },
      editor,
      "ai"
    );
  };

  const clearHighlight = (editor: Editor) => {
    setRange(null);
    setContent("");
    setPrevContent("");
    setType("selection");

    editor.chain().unsetSelectionsInDocument().focus().run();
  };

  const undo = (editor: Editor) => {
    if (!range) {
      return;
    }
    if (type === "ai") {
      editor.chain().deleteRange(range).insertContent(prevContent).run();
      setAiContextAndHighlightRange(
        { from: range.from, to: range.from + prevContent.length },
        editor,
        "selection"
      );
    }
  };

  return (
    <AiContext.Provider
      value={{
        range,
        content,
        setAiContextAndHighlightRange,
        type,
        updateContent,
        clearHighlight,
        undo,
      }}
    >
      {children}
    </AiContext.Provider>
  );
};

export default AiProvider;
