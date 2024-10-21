import { HighlightOptions } from "@tiptap/extension-highlight";

export type AIHighlightType = "ai" | "selection";

export type AIHighlightOptions = HighlightOptions & {
  type: AIHighlightType;
};

declare module "@tiptap/core" {
  interface Commands<ReturnType> {
    aiHighlight: {
      /**
       * Highlights selected text to be sent to context of ai
       */
      setSelectionHighlight: () => ReturnType;
      /**
       * Highlights newly generated text by ai
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
        type?: AIHighlightType;
      }) => ReturnType;
    };
  }
}
