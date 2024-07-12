import { createContext, useState } from "react";

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

      // Transform the grouped notifications into BulkNotification format
      const bulkNotifs: BulkNotification[] = Object.keys(bulkMap).map(
        (bulkId) => ({
          bulk_id: bulkId,
          notifications: bulkMap[bulkId],
        })
      );

      setBulkNotifications(bulkNotifs);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <NotificationsContext.Provider
      value={{
        isVisible,
        setIsVisible,
        bulkNotifications,
        setBulkNotifications,
        updateNotifications,
      }}
    >
      {children}
    </NotificationsContext.Provider>
  );
};
