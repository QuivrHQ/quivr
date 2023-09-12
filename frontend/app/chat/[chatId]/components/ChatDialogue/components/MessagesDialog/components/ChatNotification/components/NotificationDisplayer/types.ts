export type NotificationMessage = {
  message: string;
  status: "warning" | "error" | "success";
  name: string;
};
export const notificationStatusToIcon = {
  warning: "⚠️",
  error: "❌",
  success: "✅",
};
