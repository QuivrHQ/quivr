import { ThreadItemWithGroupedNotifications } from "../../../../types";
import { QADisplay } from "../QADisplay";
import { ThreadNotification } from "../ThreadNotification/ThreadNotification";

type ThreadItemProps = {
  content: ThreadItemWithGroupedNotifications;
  index: number;
};
export const ThreadItem = ({
  content,
  index,
}: ThreadItemProps): JSX.Element => {
  if (content.item_type === "MESSAGE") {
    return <QADisplay content={content.body} index={index} />;
  }

  return <ThreadNotification content={content.body} />;
};
