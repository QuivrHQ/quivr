import { ChatNotification } from "./ChatNotification/ChatNotification";
import { QADisplay } from "./QADisplay";

import { ChatItemWithGroupedNotifications } from "../../../../types";

type ChatItemProps = {
  content: ChatItemWithGroupedNotifications;
  index: number;
  lastMessage?: boolean;
};
export const ChatItem = ({
  content,
  index,
  lastMessage,
}: ChatItemProps): JSX.Element => {
  if (content.item_type === "MESSAGE") {
    return (
      <QADisplay
        content={content.body}
        index={index}
        lastMessage={lastMessage}
      />
    );
  }

  return <ChatNotification content={content.body} />;
};
