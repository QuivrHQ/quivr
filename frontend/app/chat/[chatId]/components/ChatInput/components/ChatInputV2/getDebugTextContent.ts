import { $isElementNode, LexicalNode } from "lexical";
import { $isBeautifulMentionNode } from "lexical-beautiful-mentions";

export function getDebugTextContent(node: LexicalNode) {
  const nodes = [];
  const stack = [node];
  while (stack.length > 0) {
    let hasChildren = false;
    const currentNode = stack.pop();
    if ($isElementNode(currentNode)) {
      const children = currentNode.getChildren();
      hasChildren = children.length > 0;
      stack.unshift(...children);
    }
    if (currentNode !== node && !hasChildren) {
      nodes.push(
        $isBeautifulMentionNode(currentNode)
          ? "[" + currentNode.getTextContent() + "]"
          : currentNode.getTextContent()
      );
    }
  }

  return nodes.reverse().join("");
}
