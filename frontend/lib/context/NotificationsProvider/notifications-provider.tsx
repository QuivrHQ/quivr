import { createContext, useState } from "react";

type NotificationsContextType = {
  isVisible: boolean;
  setIsVisible: React.Dispatch<React.SetStateAction<boolean>>;
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

  return (
    <NotificationsContext.Provider value={{ isVisible, setIsVisible }}>
      {children}
    </NotificationsContext.Provider>
  );
};
