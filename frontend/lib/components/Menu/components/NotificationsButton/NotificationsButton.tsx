import { useEffect } from "react";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import styles from "./NotificationsButton.module.scss";

export const NotificationsButton = (): JSX.Element => {
  const { isVisible, setIsVisible, unreadNotifications, updateNotifications } =
    useNotificationsContext();
  const { supabase } = useSupabase();

  useEffect(() => {
    const channel = supabase
      .channel("notifications")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "notifications" },
        () => {
          void updateNotifications();
        }
      )
      .subscribe();

    return () => {
      void supabase.removeChannel(channel);
    };
  }, []);

  useEffect(() => {
    void updateNotifications();
  }, []);

  return (
    <div
      className={styles.button_wrapper}
      onClick={(event) => {
        setIsVisible(!isVisible);
        event.preventDefault();
        event.nativeEvent.stopImmediatePropagation();
      }}
      id="notifications-button"
    >
      <MenuButton
        label="Notifications"
        iconName="notifications"
        type="open"
        color="primary"
      />
      {!!unreadNotifications && (
        <span className={styles.badge}>
          {unreadNotifications > 9 ? "9+" : unreadNotifications}
        </span>
      )}
    </div>
  );
};
