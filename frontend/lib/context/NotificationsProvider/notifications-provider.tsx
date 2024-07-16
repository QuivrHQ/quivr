import { createContext, useEffect, useState } from "react";

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
      setUnreadNotifications(
        bulkNotifs.filter((bulk) => !bulk.notifications[0].read).length
      );
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    void (async () => {
      for (const notifications of bulkNotifications) {
        if (
          notifications.notifications.every((notif) => notif.status !== "info")
        ) {
          for (const notification of notifications.notifications) {
            await supabase
              .from("notifications")
              .update({ read: true })
              .eq("id", notification.id);
          }
        }
      }
      await updateNotifications();
    })();
  }, [isVisible]);

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
