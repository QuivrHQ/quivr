import { Editor, Range } from "@tiptap/core";
import { createContext, useState } from "react";

export type AiContextType = {
  range: Range | null;
  content: string;
  setAiContextAndHighlightRange: (range: Range, editor: Editor) => void;
};

export const AiContext = createContext<AiContextType>({
  range: null,
  content: "",
  setAiContextAndHighlightRange: () => "",
});

const AiProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [range, setRange] = useState<Range | null>(null);
  const [content, setContent] = useState("");

  const setAiContextAndHighlightRange = (newRange: Range, editor: Editor) => {
    setRange(newRange);
    setContent(editor.state.doc.textBetween(newRange.from, newRange.to));
    editor
      .chain()
      .unsetSelectionsInDocument()
      .setTextSelection(newRange)
      .setHighlight({ type: "selection" })
      .focus(newRange.to)
      .run();
  };

  return (
    <AiContext.Provider
      value={{ range, content, setAiContextAndHighlightRange }}
    >
      {children}
    </AiContext.Provider>
  );
};

export default AiProvider;
