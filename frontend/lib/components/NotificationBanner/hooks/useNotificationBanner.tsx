import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useState } from "react";

import { NOTIFICATION_BANNER_DATA_KEY } from "@/lib/api/cms/config";
import { useCmsApi } from "@/lib/api/cms/useCmsApi";

import {
  clearLocalStorageNotificationBanner,
  getNotificationFromLocalStorage,
  setNotificationAsDismissedInLocalStorage,
} from "../utils";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useNotificationBanner = () => {
  const [isDismissed, setIsDismissed] = useState(true);

  const { getNotificationBanner } = useCmsApi();
  const { data: notificationBanner } = useQuery({
    queryKey: [NOTIFICATION_BANNER_DATA_KEY],
    queryFn: getNotificationBanner,
  });

  const dismissNotification = useCallback(() => {
    if (notificationBanner?.id === undefined) {
      return;
    }
    setNotificationAsDismissedInLocalStorage(notificationBanner.id);
    setIsDismissed(true);
  }, [notificationBanner?.id]);

  useEffect(() => {
    const localStorageNotificationBanner = getNotificationFromLocalStorage();
    if (notificationBanner === undefined) {
      return;
    }
    if (localStorageNotificationBanner?.id !== notificationBanner.id) {
      clearLocalStorageNotificationBanner();
      setIsDismissed(false);
    }
  }, [dismissNotification, notificationBanner?.id]);

  useEffect(() => {
    const onUnmount = () => {
      if (notificationBanner?.isSticky === undefined) {
        return;
      }
      if (!notificationBanner.isSticky) {
        dismissNotification();
      }
    };

    return onUnmount;
  }, [dismissNotification, notificationBanner?.isSticky]);

  return {
    notificationBanner,
    dismissNotification,
    isDismissed,
  };
};
