import { ChatItemWithGroupedNotifications } from "../../../../types";
import { ChatNotification } from "../ChatNotification/ChatNotification";
import { QADisplay } from "../QADisplay";

type ChatItemProps = {
  content: ChatItemWithGroupedNotifications;
};
export const ChatItem = ({ content }: ChatItemProps): JSX.Element => {
  if (content.item_type === "MESSAGE") {
    return <QADisplay content={content.body} />;
  }

  return <ChatNotification content={content.body} />;
};
