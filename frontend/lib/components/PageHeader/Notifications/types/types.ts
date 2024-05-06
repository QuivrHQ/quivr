export enum NotificationStatus {
  Info = "info",
  Warning = "warning",
  Error = "error",
  Success = "success",
}

export interface NotificationType {
  id: number;
  title: string;
  datetime: string;
  status: NotificationStatus;
  archived: boolean;
  read: boolean;
  description: string;
}
