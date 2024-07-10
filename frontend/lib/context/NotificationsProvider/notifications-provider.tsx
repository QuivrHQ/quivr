import { createContext, useState } from "react";

import { NotificationType } from "@/lib/components/Menu/types/types";

type NotificationsContextType = {
  isVisible: boolean;
  setIsVisible: React.Dispatch<React.SetStateAction<boolean>>;
  notifications: NotificationType[];
  setNotifications: React.Dispatch<React.SetStateAction<NotificationType[]>>;
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
  const [isVisible, setIsVisible] = useState(false);
  const [notifications, setNotifications] = useState<NotificationType[]>([]);
  const [unreadNotifications, setUnreadNotifications] = useState<number>(0);

  return (
    <NotificationsContext.Provider
      value={{
        isVisible,
        setIsVisible,
        notifications,
        setNotifications,
        unreadNotifications,
        setUnreadNotifications,
      }}
    >
      {children}
    </NotificationsContext.Provider>
  );
};
