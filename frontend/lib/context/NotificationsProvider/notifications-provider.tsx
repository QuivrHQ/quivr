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
  setBulkNotifications: React.Dispatch<
    React.SetStateAction<BulkNotification[]>
  >;
  updateNotifications: () => Promise<void>;
  unreadNotifications?: number;
  setUnreadNotifications?: React.Dispatch<React.SetStateAction<number>>;
};

export const NotificationsContext = createContext<
  NotificationsContextType | undefined
>(undefined);

export const NotificationsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isVisible, setIsVisible] = useState(false);
  const [unreadNotifications, setUnreadNotifications] = useState(0);
  const [bulkNotifications, setBulkNotifications] = useState<
    BulkNotification[]
  >([]);
  const { supabase } = useSupabase();

  const updateNotifications = async () => {
    try {
      const lastRetrieved = localStorage.getItem("lastRetrieved");
      const now = Date.now();

      if (lastRetrieved && now - parseInt(lastRetrieved) < 1000) {

        return;
      }

      localStorage.setItem("lastRetrieved", now.toString());

      let notifs = (await supabase.from("notifications").select()).data;
      if (notifs) {
        notifs = notifs.sort(
          (a: NotificationType, b: NotificationType) =>
            new Date(b.datetime).getTime() - new Date(a.datetime).getTime()
        );
      }

      const bulkMap: { [key: string]: NotificationType[] } = {};
      notifs?.forEach((notif: NotificationType) => {
        if (!bulkMap[notif.bulk_id]) {
          bulkMap[notif.bulk_id] = [];
        }
        bulkMap[notif.bulk_id].push(notif);
      });

      const bulkNotifs: BulkNotification[] = Object.keys(bulkMap).map(
        (bulkId) => ({
          bulk_id: bulkId,
          notifications: bulkMap[bulkId],
          category: bulkMap[bulkId][0].category,
          brain_id: bulkMap[bulkId][0].brain_id,
          datetime: bulkMap[bulkId][0].datetime,
        })
      );

      setBulkNotifications(bulkNotifs);

      const unreadCount = bulkNotifs.filter((bulk) => !bulk.notifications[0].read).length;
      setUnreadNotifications(unreadCount);
    } catch (error) {
    }
  };

  const debounce = (func: Function, delay: number) => {
    let timeoutId: NodeJS.Timeout;
    let lastArgs: any[];

    const debouncedFunction = (...args: any[]) => {
      lastArgs = args;
      if (timeoutId) { clearTimeout(timeoutId); }
      timeoutId = setTimeout(() => {
        func(...lastArgs);
      }, delay);
    };

    debouncedFunction.cancel = () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };

    return debouncedFunction;
  };

  const debouncedUpdateNotifications = useCallback(
    debounce(() => {
      console.log("⏳ Debouncing updateNotifications call");
      updateNotifications();
    }, 1000), // Adjusted the delay to 1 second
    [updateNotifications] // Ensure updateNotifications is a dependency
  );

  useEffect(() => {
    if (isVisible) {
      const lastRetrieved = localStorage.getItem("lastRetrieved");
      const now = Date.now();

      // Only call debouncedUpdateNotifications if the last retrieval was more than 1 second ago
      if (!lastRetrieved || now - parseInt(lastRetrieved) >= 1000) {
        debouncedUpdateNotifications();
      }

      // Add a cleanup function to clear the timeout when the component unmounts or isVisible changes
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
      }}
    >
      {children}
    </NotificationsContext.Provider>
  );
};
