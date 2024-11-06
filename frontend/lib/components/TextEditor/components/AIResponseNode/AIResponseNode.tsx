import { NodeViewProps } from "@tiptap/core";
import { NodeViewContent, NodeViewWrapper } from "@tiptap/react";

import styles from "./AIResponseNode.module.scss";

import { QuivrButton } from "../../../ui/QuivrButton/QuivrButton";

const AIResponseNode = (props: NodeViewProps): JSX.Element => {
  const { attrs, content } = props.node;
  const { editor } = props;

  return (
    <NodeViewWrapper className={styles.wrapper}>
      {attrs.context && <div className={styles.context}>{attrs.context}</div>}
      <NodeViewContent className={styles.content} />
      <div className={styles.actions_wrapper}>
        <QuivrButton
          color="primary"
          iconName="check"
          label="Accept"
          onClick={() => {
            editor.commands.acceptAiResponse({
              content: content.textBetween(0, content.size),
            });
          }}
        />
        <QuivrButton
          color="dangerous"
          iconName="close"
          label="Decline"
          onClick={() => {
            editor.commands.declineAiResponse({
              prevContent: attrs.context as string,
            });
          }}
        />
      </div>
    </NodeViewWrapper>
  );
};

export default AIResponseNode;
