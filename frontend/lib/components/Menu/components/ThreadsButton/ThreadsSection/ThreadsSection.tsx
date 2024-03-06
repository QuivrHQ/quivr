import { ThreadEntity } from "@/app/thread/[threadId]/types";

import { ThreadItem } from "./ThreadItem/ThreadItem";
import styles from "./ThreadsSection.module.scss";

type ThreadSectionProps = {
  threads: ThreadEntity[];
  title: string;
};

export const ThreadsSection = (props: ThreadSectionProps): JSX.Element => {
  if (props.threads.length === 0) {
    return <></>;
  }

  return (
    <div>
      <div>{props.title}</div>
      <div className={styles.threads_wrapper}>
        {props.threads.map((thread) => (
          <ThreadItem key={thread.thread_id} threadHistoryItem={thread} />
        ))}
      </div>
    </div>
  );
};
