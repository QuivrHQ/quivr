import { Notification, ThreadMessageItem } from "../../types";

export type ThreadItemWithGroupedNotifications =
  | ThreadMessageItem
  | {
      item_type: "NOTIFICATION";
      body: Notification[];
    };
