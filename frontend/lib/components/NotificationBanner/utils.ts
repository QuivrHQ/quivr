const notificationsLocalStorageKey = "homepage-notifications";

type LocalStorageNotification = {
  isDismissed: boolean;
  id: string;
};

export const getNotificationFromLocalStorage = ():
  | LocalStorageNotification
  | undefined => {
  const notifications = localStorage.getItem(notificationsLocalStorageKey);

  if (notifications !== null) {
    return JSON.parse(notifications) as LocalStorageNotification;
  }

  return undefined;
};

export const setNotificationAsDismissedInLocalStorage = (id: string): void => {
  const notificationPayload: LocalStorageNotification = {
    isDismissed: true,
    id,
  };
  localStorage.setItem(
    notificationsLocalStorageKey,
    JSON.stringify(notificationPayload)
  );
};

export const clearLocalStorageNotificationBanner = (): void => {
  localStorage.removeItem(notificationsLocalStorageKey);
};
