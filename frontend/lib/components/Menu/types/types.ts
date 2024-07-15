import { UUID } from "crypto";

export enum NotificationStatus {
  Info = "info",
  Warning = "warning",
  Error = "error",
  Success = "success",
}

export interface BulkNotification {
  notifications: NotificationType[];
  bulk_id: string;
  category: "sync" | "upload" | "crawl";
  brain_id: UUID;
}

export interface NotificationType {
  id: string;
  title: string;
  datetime: string;
  status: NotificationStatus;
  archived: boolean;
  read: boolean;
  description: string;
  bulk_id: string;
  category: "sync" | "upload" | "crawl";
  brain_id: UUID;
}
