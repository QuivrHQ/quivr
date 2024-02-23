import { ChatItemWithGroupedNotifications } from "../../../../types";
import { ChatNotification } from "../ChatNotification/ChatNotification";
import { QADisplay } from "../QADisplay";

type ChatItemProps = {
  content: ChatItemWithGroupedNotifications;
  index: number;
};
export const ChatItem = ({ content, index }: ChatItemProps): JSX.Element => {
  if (content.item_type === "MESSAGE") {
    return <QADisplay content={content.body} index={index} />;
  }

  return <ChatNotification content={content.body} />;
};
