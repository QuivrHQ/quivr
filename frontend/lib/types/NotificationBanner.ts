import { HTMLAttributes } from "react";

export type NotificationBanner = {
  id: string;
  text: string;
  style?: HTMLAttributes<HTMLDivElement>["style"];
  dismissible?: boolean;
  isSticky?: boolean;
};
