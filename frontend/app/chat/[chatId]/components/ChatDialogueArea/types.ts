import { ChatMessageItem, Notification } from "../../types";

export type ChatItemWithGroupedNotifications =
  | ChatMessageItem
  | {
      item_type: "NOTIFICATION";
      body: Notification[];
    };
