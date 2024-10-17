import { Command } from "@tiptap/core";
import { Highlight } from "@tiptap/extension-highlight";

import { AIHighlightOptions } from "./types";

const unsetSelectionsInDocument: Command = ({ dispatch, state }) => {
  const { tr } = state;
  if (!dispatch) {
    return false;
  }

  state.doc.descendants((node, pos) => {
    if (node.isText) {
      node.marks.forEach((mark) => {
        if (mark.type.name === "aiHighlight") {
          if (mark.attrs["type"] !== "selection") {
            return false;
          }

          tr.removeMark(pos, pos + node.nodeSize, mark.type);
        }
      });
    }
  });

  dispatch(tr);

  return true;
};

export const AIHighlight = Highlight.extend<AIHighlightOptions>({
  name: "aiHighlight",
  addAttributes() {
    return {
      ...this.parent?.(),
      type: "selection",
    };
  },
  addCommands() {
    return {
      ...this.parent?.(),
      unsetSelectionsInDocument: () => unsetSelectionsInDocument,
      setSelectionHighlight: () => {
        return ({ commands }) => {
          return commands.setHighlight({ type: "selection" });
        };
      },
      setAiHighlight: () => {
        return ({ commands }) => {
          return commands.setHighlight({ type: "ai" });
        };
      },
    };
  },
  onSelectionUpdate() {
    this.editor.commands.unsetSelectionsInDocument();
  },
}).configure({
  multicolor: true,
  type: "selection",
});
