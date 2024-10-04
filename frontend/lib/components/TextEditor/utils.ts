import { Editor } from "@tiptap/core";

export const unsetMarkInDocument = (
  editor: Editor,
  markType: string,
  attrs?: { [k: string]: string | boolean | number }
): void => {
  const { state, view } = editor;
  const { tr } = state;

  state.doc.descendants((node, pos) => {
    if (node.isText) {
      node.marks.forEach((mark) => {
        if (mark.type.name === markType) {
          if (attrs !== undefined) {
            for (const attr in attrs) {
              // eslint-disable-next-line max-depth
              if (mark.attrs[attr] !== attrs[attr]) {
                return;
              }
            }
          }

          tr.removeMark(pos, pos + node.nodeSize, mark.type);
        }
      });
    }
  });

  view.dispatch(tr);
};
