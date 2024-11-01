import { Command } from "@tiptap/core";
import { Highlight } from "@tiptap/extension-highlight";

const unsetSelectionsInDocument: Command = ({ dispatch, state }) => {
  const { tr } = state;
  if (!dispatch) {
    return false;
  }

  state.doc.descendants((node, pos) => {
    if (node.isText) {
      node.marks.map((mark) => {
        if (mark.type.name === AIHighlight.name) {
          tr.removeMark(pos, pos + node.nodeSize, mark.type);
        }
      });
    }
  });

  dispatch(tr);

  return true;
};

export const AIHighlight = Highlight.extend({
  name: "aiHighlight",

  addCommands() {
    return {
      ...this.parent?.(),
      unsetSelectionsInDocument: () => unsetSelectionsInDocument,
      setSelectionHighlight: () => {
        return ({ commands }) => {
          return commands.setHighlight();
        };
      },
    };
  },

  onSelectionUpdate() {
    this.editor.commands.unsetSelectionsInDocument();
  },
}).configure({
  multicolor: true,
});
