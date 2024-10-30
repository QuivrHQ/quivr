import { Editor, Range } from "@tiptap/core";
import { createContext, Dispatch, SetStateAction, useState } from "react";

export type AiContextType = {
  range: Range | null;
  aiContext: string;
  setAiContextAndHighlightRange: (range: Range, editor: Editor) => void;
  clearHighlight: (editor: Editor) => void;
  deleteContent: (editor: Editor) => void;
  restorePrev: (editor: Editor) => void;
  setAiContext: Dispatch<SetStateAction<string>>;
};

export const AiContext = createContext<AiContextType | null>(null);

const AiProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [range, setRange] = useState<Range | null>(null);
  const [aiContext, setAiContext] = useState("");
  const [prevAiContext, setPrevAiContext] = useState("");

  const setAiContextAndHighlightRange = (newRange: Range, editor: Editor) => {
    setRange(newRange);
    setPrevAiContext(aiContext);
    setAiContext(editor.state.doc.textBetween(newRange.from, newRange.to));
    editor
      .chain()
      .unsetSelectionsInDocument()
      .setTextSelection(newRange)
      .setHighlight({ type: "selection" })
      .focus(newRange.to)
      .run();
  };

  const clearHighlight = (editor: Editor) => {
    if (!range) {
      return;
    }
    editor
      .chain()
      .setTextSelection(range)
      .unsetHighlight()
      .setTextSelection(range.to)
      .focus()
      .run();

    setRange(null);
    setPrevAiContext(aiContext);
    setAiContext("");
  };

  const restorePrev = (editor: Editor) => {
    editor.chain().insertContent(prevAiContext).run();
    // setAiContextAndHighlightRange(
    //   { from: range.from, to: range.from + prevContent.length },
    //   editor,
    //   "selection"
    // );
  };

  const deleteContent = (editor: Editor) => {
    if (!range) {
      return;
    }
    editor.chain().deleteRange(range).focus(range.from).run();
    setRange(null);
    setPrevAiContext(aiContext);
    setAiContext("");
  };

  return (
    <AiContext.Provider
      value={{
        range,
        aiContext,
        setAiContextAndHighlightRange,
        restorePrev,
        clearHighlight,
        deleteContent,
        setAiContext,
      }}
    >
      {children}
    </AiContext.Provider>
  );
};

export default AiProvider;
