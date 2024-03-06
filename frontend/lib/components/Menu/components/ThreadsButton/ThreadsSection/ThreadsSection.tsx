import { ThreadEntity } from "@/app/thread/[threadId]/types";

import { ThreadItem } from "./ThreadItem/ThreadItem";
import styles from "./ThreadsSection.module.scss";

type ThreadSectionProps = {
  chats: ThreadEntity[];
  title: string;
};

export const ThreadsSection = (props: ThreadSectionProps): JSX.Element => {
  if (props.chats.length === 0) {
    return <></>;
  }

  return (
    <div>
      <div>{props.title}</div>
      <div className={styles.chats_wrapper}>
        {props.chats.map((chat) => (
          <ThreadItem key={chat.chat_id} chatHistoryItem={chat} />
        ))}
      </div>
    </div>
  );
};
