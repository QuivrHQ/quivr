import { Editor, Range } from "@tiptap/core";
import { createContext, useState } from "react";

import { AIHighlightType } from "../extensions/types";

export type AiContextType = {
  range: Range | null;
  content: string;
  type: AIHighlightType;
  setAiContextAndHighlightRange: (range: Range, editor: Editor) => void;
  updateContent: (newContent: string, editor: Editor) => void;
};

export const AiContext = createContext<AiContextType | null>(null);

const AiProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [range, setRange] = useState<Range | null>(null);
  const [content, setContent] = useState("");
  const [type, setType] = useState<AIHighlightType>("selection");

  const setAiContextAndHighlightRange = (
    newRange: Range,
    editor: Editor,
    newType: AIHighlightType = "selection"
  ) => {
    setRange(newRange);
    console.log({
      from: newRange.from,
      to: newRange.to,
      content,
      newType,
    });
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

  return (
    <AiContext.Provider
      value={{
        range,
        content,
        setAiContextAndHighlightRange,
        type,
        updateContent,
      }}
    >
      {children}
    </AiContext.Provider>
  );
};

export default AiProvider;
