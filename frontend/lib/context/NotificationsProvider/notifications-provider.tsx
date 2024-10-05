import { createContext, useCallback, useEffect, useState } from "react";

import {
  BulkNotification,
  NotificationType,
} from "@/lib/components/Menu/types/types";

import { useSupabase } from "../SupabaseProvider";

type NotificationsContextType = {
  isVisible: boolean;
  setIsVisible: React.Dispatch<React.SetStateAction<boolean>>;
  bulkNotifications: BulkNotification[];
  setBulkNotifications: React.Dispatch<React.SetStateAction<BulkNotification[]>>;
  updateNotifications: () => Promise<void>;
  unreadNotifications: number;
  setUnreadNotifications: React.Dispatch<React.SetStateAction<number>>;
};

export const NotificationsContext = createContext<NotificationsContextType | undefined>(undefined);

export const NotificationsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isVisible, setIsVisible] = useState<boolean>(false);
  const [unreadNotifications, setUnreadNotifications] = useState<number>(0);
  const [bulkNotifications, setBulkNotifications] = useState<BulkNotification[]>([]);
  const { supabase } = useSupabase();

  const fetchNotifications = async (): Promise<NotificationType[]> => {
    const { data, error } = await supabase.from("notifications").select();
    if (error) {

      return [];
    }

    // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unnecessary-condition
    return data || [];
  };

  const processNotifications = (notifications: NotificationType[]): BulkNotification[] => {
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
      const lastRetrieved = localStorage.getItem("lastRetrieved");
      const now = Date.now();

      if (lastRetrieved && now - parseInt(lastRetrieved) < 1000) {

        return;
      }

      localStorage.setItem("lastRetrieved", now.toString());

      const notifications = await fetchNotifications();
      const sortedNotifications = notifications.sort(
        (a, b) => new Date(b.datetime).getTime() - new Date(a.datetime).getTime()
      );

      const bulkNotifs = processNotifications(sortedNotifications);
      setBulkNotifications(bulkNotifs);

      const unreadCount = bulkNotifs.filter((bulk) => !bulk.notifications[0].read).length;
      setUnreadNotifications(unreadCount);
    } catch (error) {
      console.error("Error updating notifications:", error);
    }
  };

  const debounce = <T extends (...args: unknown[]) => void>(func: T, delay: number): T & { cancel: () => void } => {
    let timeoutId: NodeJS.Timeout; // Holds the timeout ID for the current debounce delay
    let lastArgs: Parameters<T>; // Stores the last arguments passed to the debounced function

    const debouncedFunction = (...args: Parameters<T>) => {
      lastArgs = args; // Update the last arguments with the current call's arguments
      // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
      if (timeoutId) {
        clearTimeout(timeoutId); // Clear the existing timeout if it exists
      }
      // Set a new timeout to call the function after the specified delay
      timeoutId = setTimeout(() => {
        func(...lastArgs); // Call the function with the last arguments
      }, delay);
    };

    debouncedFunction.cancel = () => {
      // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
      if (timeoutId) {
        clearTimeout(timeoutId); // Clear the timeout if the debounced function is canceled
      }
    };

    return debouncedFunction as T & { cancel: () => void }; // Return the debounced function with a cancel method
  };

  const debouncedUpdateNotifications = useCallback(
    // eslint-disable-next-line @typescript-eslint/no-misused-promises
    debounce(updateNotifications, 1000),
    [updateNotifications]
  );

  useEffect(() => {
    if (isVisible) {
      const lastRetrieved = localStorage.getItem("lastRetrieved");
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
