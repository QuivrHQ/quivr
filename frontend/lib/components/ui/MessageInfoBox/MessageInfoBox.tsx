import styles from "./MessageInfoBox.module.scss";

import { Icon } from "../Icon/Icon";

export type MessageInfoBoxProps = {
  content: string;
};

export const MessageInfoBox = ({
  content,
}: MessageInfoBoxProps): JSX.Element => {
  return (
    <div className={styles.message_info_box_wrapper}>
      <Icon name="info" size="normal" color="grey" />
      <span>{content}</span>
    </div>
  );
};
