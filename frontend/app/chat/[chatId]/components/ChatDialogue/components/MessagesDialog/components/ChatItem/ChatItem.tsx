import { ChatItemWithGroupedNotifications } from "../../../../types";
import { ChatNotification } from "../ChatNotification/ChatNotification";
import { QADisplay } from "../QADisplay";

type ChatItemProps = {
  content: ChatItemWithGroupedNotifications;
};
export const ChatItem = ({ content }: ChatItemProps): JSX.Element => {
  if (content.item_type === "MESSAGE") {
    return <QADisplay key={content.body.message_id} content={content.body} />;
  }

  return <ChatNotification key={content.body[0].id} content={content.body} />;
};
