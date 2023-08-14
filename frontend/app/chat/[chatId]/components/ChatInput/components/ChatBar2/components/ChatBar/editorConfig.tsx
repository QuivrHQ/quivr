import { InitialConfigType } from "@lexical/react/LexicalComposer";
import { $createParagraphNode, $getRoot } from "lexical";
import {
  $convertToMentionNodes,
  BeautifulMentionNode,
  ZeroWidthNode,
} from "lexical-beautiful-mentions";

import { MentionItem } from "../../../ActionsBar/components";
import { theme } from "./helpers/theme";

function setEditorState(initialValue: string, triggers: string[]) {
  return () => {
    const root = $getRoot();
    if (root.getFirstChild() === null) {
      const paragraph = $createParagraphNode();
      console.log({
        initialValue,
        triggers,
      });
      paragraph.append(...$convertToMentionNodes(initialValue, triggers));
      root.append(paragraph);
    }
  };
}

class CustomMention extends BeautifulMentionNode {
  static getType() {
    return "custom-mention";
  }

  decorate() {
    const textContent = this.getTextContent();

    const onRemove = () => {
      alert("Hello");
    };

    console.log({ textContent });

    return <MentionItem text={textContent} onRemove={onRemove} prefix={""} />;
  }
}

export const editorConfig = (
  triggers: string[],
  initialValue: string
): InitialConfigType => ({
  namespace: "",
  theme,
  onError(error: any) {
    throw error;
  },
  editorState: setEditorState(initialValue, triggers),
  nodes: [
    BeautifulMentionNode,
    ZeroWidthNode,
    CustomMention,
    {
      replace: BeautifulMentionNode,
      with: (node: BeautifulMentionNode) => {
        return new CustomMention(node.__trigger, node.__value, node.__data);
      },
    },
  ],
});
