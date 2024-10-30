import { NodeViewProps } from "@tiptap/core";
import { NodeViewContent, NodeViewWrapper } from "@tiptap/react";

import styles from "./AIResponseNode.module.scss";

import { QuivrButton } from "../../../ui/QuivrButton/QuivrButton";

const AIResponseNode = (props: NodeViewProps): JSX.Element => {
  return (
    <NodeViewWrapper className={styles.wrapper}>
      <div className={styles.context}>{props.node.attrs.context}</div>
      <NodeViewContent className={styles.content} />
      <div className={styles.actions_wrapper}>
        <QuivrButton
          color="primary"
          iconName="check"
          label="Accept"
          onClick={() => {
            props.editor.commands.acceptAiResponse({
              content: props.node.content.textBetween(
                0,
                props.node.content.size
              ),
            });
          }}
        />
        <QuivrButton
          color="dangerous"
          iconName="close"
          label="Decline"
          onClick={() => {
            props.editor.commands.declineAiResponse({
              prevContent: props.node.attrs.context as string,
            });
          }}
        />
      </div>
    </NodeViewWrapper>
  );
};

export default AIResponseNode;
