import { mergeAttributes, Node } from "@tiptap/core";
import { ReactNodeViewRenderer } from "@tiptap/react";

import { AIResponseOptions } from "./types";

import AIResponseNode from "../components/AIResponseNode/AIResponseNode";

export const AiResponse = Node.create<AIResponseOptions>({
  name: "aiResponse",
  group: "block",
  content: "inline*",

  addAttributes() {
    return {
      ...this.parent?.(),
      context: {
        default: "",
      },
    };
  },

  renderHTML: ({ HTMLAttributes }) => {
    return ["ai-response", mergeAttributes(HTMLAttributes)];
  },

  parseHTML: () => {
    return [
      {
        tag: "ai-response",
      },
    ];
  },

  addCommands() {
    return {
      ...this.parent?.(),
      createAiResponse:
        ({ content, context }: { content: string; context: string }) =>
        ({ chain }) => {
          return chain()
            .insertContent({
              type: this.name,
              attrs: { context },
              content: [
                {
                  type: "text",
                  text: content,
                },
              ],
            })
            .focus()
            .run();
        },
      acceptAiResponse:
        ({ content }: { content: string }) =>
        ({ chain }) => {
          return chain()
            .deleteNode(this.name)
            .insertContent({
              type: "paragraph",
              content: [
                {
                  type: "text",
                  text: content,
                },
              ],
            })
            .run();
        },
      declineAiResponse:
        ({ prevContent }: { prevContent: string }) =>
        ({ chain }) => {
          return chain()
            .deleteNode(this.name)
            .insertContent({
              type: "paragraph",
              content: [
                {
                  type: "text",
                  text: prevContent,
                },
              ],
            })
            .run();
        },
    };
  },

  addNodeView: () => {
    return ReactNodeViewRenderer(AIResponseNode);
  },
});
