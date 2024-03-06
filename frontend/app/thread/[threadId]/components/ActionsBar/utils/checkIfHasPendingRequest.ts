import { Notification } from "../../../types";

export const checkIfHasPendingRequest = (
  notifications: Notification[]
): boolean => {
  return notifications.some((item) => item.status === "Pending");
};
