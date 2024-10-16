import { HighlightOptions } from "@tiptap/extension-highlight";

export type AIHighlightOptions = HighlightOptions & {
  type: "ai" | "selection";
};

declare module "@tiptap/core" {
  interface Commands<ReturnType> {
    aiHighlight: {
      /**
       * Highlights selected text to be sent to context of ai
       */
      setSelectionHighlight: () => ReturnType;
      /**
       * Highlights selected text to be sent to context of ai
       */
      setAiHighlight: () => ReturnType;
      /**
       * Remove highlights in selection
       */
      unsetSelectionsInDocument: () => ReturnType;
      /**
       * Set a highlight mark
       * @param attributes The highlight attributes
       * @example editor.commands.setHighlight({ color: 'red' })
       */
      setHighlight: (attributes?: {
        color?: string;
        type?: "selection" | "ai";
      }) => ReturnType;
    };
  }
}
