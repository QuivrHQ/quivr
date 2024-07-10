import { createContext, useState } from "react";

import { NotificationType } from "@/lib/components/Menu/types/types";

import { useSupabase } from "../SupabaseProvider";

type NotificationsContextType = {
  isVisible: boolean;
  setIsVisible: React.Dispatch<React.SetStateAction<boolean>>;
  notifications: NotificationType[];
  setNotifications: React.Dispatch<React.SetStateAction<NotificationType[]>>;
  unreadNotifications: number;
  setUnreadNotifications: React.Dispatch<React.SetStateAction<number>>;
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
  const [notifications, setNotifications] = useState<NotificationType[]>([]);
  const [unreadNotifications, setUnreadNotifications] = useState<number>(0);
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
      setNotifications(notifs ?? []);
      setUnreadNotifications(
        notifs?.filter((n: NotificationType) => !n.read).length ?? 0
      );
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <NotificationsContext.Provider
      value={{
        isVisible,
        setIsVisible,
        notifications,
        setNotifications,
        unreadNotifications,
        setUnreadNotifications,
        updateNotifications,
      }}
    >
      {children}
    </NotificationsContext.Provider>
  );
};
