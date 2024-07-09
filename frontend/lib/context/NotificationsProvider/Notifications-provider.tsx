import { createContext, useState } from "react";

import { NotificationType } from "@/lib/components/PageHeader/Notifications/types/types";

type NotificationsContextType = {
  notifications: NotificationType[];
  setNotifications: React.Dispatch<React.SetStateAction<NotificationType[]>>;
};

export const NotificationsContext = createContext<
  NotificationsContextType | undefined
>(undefined);

export const NotificationsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [notifications, setNotifications] = useState<NotificationType[]>([]);

  return (
    <NotificationsContext.Provider
      value={{
        notifications,
        setNotifications,
      }}
    >
      {children}
    </NotificationsContext.Provider>
  );
};
