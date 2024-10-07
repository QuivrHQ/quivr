import { createContext, useCallback, useEffect, useState } from "react";

import {
  BulkNotification,
  NotificationType,
} from "@/lib/components/Menu/types/types";

import { useSupabase } from "../SupabaseProvider";

const LAST_RETRIEVED_KEY = "lastRetrieved";

type NotificationsContextType = {
  isVisible: boolean;
  setIsVisible: React.Dispatch<React.SetStateAction<boolean>>;
  bulkNotifications: BulkNotification[];
  setBulkNotifications: React.Dispatch<
    React.SetStateAction<BulkNotification[]>
  >;
  updateNotifications: () => Promise<void>;
  unreadNotifications: number;
  setUnreadNotifications: React.Dispatch<React.SetStateAction<number>>;
};

export const NotificationsContext = createContext<
  NotificationsContextType | undefined
>(undefined);

export const NotificationsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isVisible, setIsVisible] = useState<boolean>(false);
  const [unreadNotifications, setUnreadNotifications] = useState<number>(0);
  const [bulkNotifications, setBulkNotifications] = useState<
    BulkNotification[]
  >([]);
  const { supabase } = useSupabase();

  const fetchNotifications = async (): Promise<NotificationType[]> => {
    const { data, error } = await supabase.from("notifications").select();

    return error ? [] : (data as NotificationType[]);
  };

  const processNotifications = (
    notifications: NotificationType[]
  ): BulkNotification[] => {
    const bulkMap: { [key: string]: NotificationType[] } = {};
    notifications.forEach((notif) => {
      if (!bulkMap[notif.bulk_id]) {
        bulkMap[notif.bulk_id] = [];
      }
      bulkMap[notif.bulk_id].push(notif);
    });

    return Object.keys(bulkMap).map((bulkId) => ({
      bulk_id: bulkId,
      notifications: bulkMap[bulkId],
      category: bulkMap[bulkId][0].category,
      brain_id: bulkMap[bulkId][0].brain_id,
      datetime: bulkMap[bulkId][0].datetime,
    }));
  };

  const updateNotifications = async (): Promise<void> => {
    try {
      const lastRetrieved = localStorage.getItem(LAST_RETRIEVED_KEY);
      const now = Date.now();

      if (lastRetrieved && now - parseInt(lastRetrieved) < 1000) {
        return;
      }

      localStorage.setItem(LAST_RETRIEVED_KEY, now.toString());

      const notifications = await fetchNotifications();
      const sortedNotifications = notifications.sort(
        (a, b) =>
          new Date(b.datetime).getTime() - new Date(a.datetime).getTime()
      );

      const bulkNotifs = processNotifications(sortedNotifications);
      setBulkNotifications(bulkNotifs);

      const unreadCount = bulkNotifs.filter(
        (bulk) => !bulk.notifications[0].read
      ).length;
      setUnreadNotifications(unreadCount);
    } catch (error) {
      console.error("Error updating notifications:", error);
    }
  };

  const debounce = <T extends (...args: unknown[]) => void>(
    func: T,
    delay: number
  ): T & { cancel: () => void } => {
    let timer: NodeJS.Timeout | undefined = undefined;
    let lastArgs: Parameters<T>;

    const debouncedFunction = (...args: Parameters<T>) => {
      lastArgs = args;
      if (timer) {
        clearTimeout(timer);
      }
      timer = setTimeout(() => {
        func(...lastArgs);
      }, delay);
    };

    debouncedFunction.cancel = () => {
      if (timer) {
        clearTimeout(timer);
      }
    };

    return debouncedFunction as T & { cancel: () => void };
  };

  const debouncedUpdateNotifications = useCallback(
    debounce(() => {
      void updateNotifications();
    }, 1000),
    [updateNotifications]
  );

  useEffect(() => {
    if (isVisible) {
      const lastRetrieved = localStorage.getItem(LAST_RETRIEVED_KEY);
      const now = Date.now();

      if (!lastRetrieved || now - parseInt(lastRetrieved) >= 1000) {
        void debouncedUpdateNotifications();
      }

      return () => {
        debouncedUpdateNotifications.cancel();
      };
    }
  }, [isVisible, debouncedUpdateNotifications]);

  return (
    <NotificationsContext.Provider
      value={{
        isVisible,
        setIsVisible,
        bulkNotifications,
        setBulkNotifications,
        updateNotifications,
        unreadNotifications,
        setUnreadNotifications,
      }}
    >
      {children}
    </NotificationsContext.Provider>
  );
};
