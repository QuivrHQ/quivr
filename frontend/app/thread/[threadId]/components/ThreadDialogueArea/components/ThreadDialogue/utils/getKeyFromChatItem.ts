import { ThreadItemWithGroupedNotifications } from "../../../types";

export const getKeyFromThreadItem = (
  threadItem: ThreadItemWithGroupedNotifications
): string => {
  if (threadItem.item_type === "MESSAGE") {
    return threadItem.body.message_id;
  } else {
    return threadItem.body[0].id;
  }
};
