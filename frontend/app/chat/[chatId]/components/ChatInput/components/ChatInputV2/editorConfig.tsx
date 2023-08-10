import { InitialConfigType } from "@lexical/react/LexicalComposer";
import { $createParagraphNode, $getRoot, ParagraphNode } from "lexical";
import {
  $convertToMentionNodes,
  BeautifulMentionNode,
  ZeroWidthNode,
} from "lexical-beautiful-mentions";

import ShowcaseTheme from "./theme";

export const defaultInitialValue =
  "Hey @John, the task is #urgent and due:tomorrow";

function setEditorState(initialValue: string, triggers: string[]) {
  return () => {
    const root = $getRoot();
    if (root.getFirstChild() === null) {
      const paragraph = $createParagraphNode();
      paragraph.append(...$convertToMentionNodes(initialValue, triggers));
      root.append(paragraph);
    }
  };
}

export class CustomMention extends ParagraphNode {
  static getType() {
    return "custom-paragraph";
  }

  static clone(node) {
    return new CustomParagraphNode(node.__key);
  }

  createDOM(config) {
    const dom = super.createDOM(config);
    dom.style = "background: green";

    return dom;
  }
}

export const editorConfig = (
  triggers: string[],
  initialValue: string
): InitialConfigType => ({
  namespace: "",
  theme: ShowcaseTheme,
  onError(error: any) {
    throw error;
  },
  editorState: setEditorState(initialValue, triggers),
  nodes: [
    BeautifulMentionNode,
    ZeroWidthNode,
    CustomMention,
    /*{
      replace: BeautifulMentionNode,
      with: (node: ParagraphNode) => {
        return new CustomMention();
      },
    },*/
  ],
});
