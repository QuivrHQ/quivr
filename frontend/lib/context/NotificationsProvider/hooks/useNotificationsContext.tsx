import { useContext } from "react";

import { NotificationsContext } from "../notifications-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useNotificationsContext = () => {
  const context = useContext(NotificationsContext);
  if (context === undefined) {
    throw new Error(
      "useNotificationsContext must be used within a MenuProvider"
    );
  }

  return context;
};
