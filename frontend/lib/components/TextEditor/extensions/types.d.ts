import { HighlightOptions } from "@tiptap/extension-highlight";

export type AIResponseOptions = HighlightOptions & {
  context: string;
};

declare module "@tiptap/core" {
  interface Commands<ReturnType> {
    aiHighlight: {
      /**
       * Highlights selected text to be sent to context of ai
       */
      setSelectionHighlight: () => ReturnType;
      /**
       * Remove highlights in selection
       */
      unsetSelectionsInDocument: () => ReturnType;
    };
    aiResponse: {
      createAiResponse: ({ content: string, context: string }) => ReturnType;
      acceptAiResponse: ({ content: string }) => ReturnType;
      declineAiResponse: ({ prevContent: string }) => ReturnType;
    };
  }
}
