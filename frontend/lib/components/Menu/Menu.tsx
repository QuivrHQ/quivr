import { MotionConfig } from "framer-motion";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { MenuControlButton } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/MenuControlButton/MenuControlButton";
import { useChatsList } from "@/app/chat/[chatId]/hooks/useChatsList";
import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { nonProtectedPaths } from "@/lib/config/routesConfig";
import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

import styles from "./Menu.module.scss";
import { AnimatedDiv } from "./components/AnimationDiv";
import { DiscussionButton } from "./components/DiscussionButton/DiscussionButton";
import { HomeButton } from "./components/HomeButton/HomeButton";
import { Notification } from "./components/Notification/Notification";
import { NotificationsButton } from "./components/NotificationsButton/NotificationsButton";
import { ProfileButton } from "./components/ProfileButton/ProfileButton";
import { SocialsButtons } from "./components/SocialsButtons/SocialsButtons";
import { StudioButton } from "./components/StudioButton/StudioButton";
import { ThreadsButton } from "./components/ThreadsButton/ThreadsButton";
import { UpgradeToPlusButton } from "./components/UpgradeToPlusButton/UpgradeToPlusButton";
import { NotificationType } from "./types/types";

import { TextButton } from "../ui/TextButton/TextButton";

export const Menu = (): JSX.Element => {
  const { isOpened } = useMenuContext();
  const {
    isVisible,
    setNotifications,
    notifications,
    setUnreadNotifications,
    unreadNotifications,
    setIsVisible,
  } = useNotificationsContext();
  const router = useRouter();
  const pathname = usePathname() ?? "";
  const [isLogoHovered, setIsLogoHovered] = useState<boolean>(false);
  const { isDarkMode } = useUserSettingsContext();
  const { supabase } = useSupabase();

  useChatsList();

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

  const deleteAllNotifications = async () => {
    for (const notification of notifications) {
      await supabase.from("notifications").delete().eq("id", notification.id);
    }
    await updateNotifications();
  };

  const markAllAsRead = async () => {
    for (const notification of notifications) {
      await supabase
        .from("notifications")
        .update({ read: true })
        .eq("id", notification.id);
    }
    await updateNotifications();
  };

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
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Node;
      const panel = document.getElementById("notifications-panel");

      if (!panel?.contains(target)) {
        setIsVisible(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    void updateNotifications();
  });

  if (nonProtectedPaths.includes(pathname)) {
    return <></>;
  }

  const displayedOnPages = [
    "/assistants",
    "/chat",
    "/library",
    "/search",
    "studio",
    "/user",
  ];

  const isMenuDisplayed = displayedOnPages.some((page) =>
    pathname.includes(page)
  );

  if (!isMenuDisplayed) {
    return <></>;
  }

  return (
    <div>
      <MotionConfig transition={{ mass: 1, damping: 10, duration: 0.1 }}>
        <div className={styles.menu_container}>
          <AnimatedDiv>
            <div className={styles.menu_wrapper}>
              <div
                className={styles.quivr_logo_wrapper}
                onClick={() => router.push("/search")}
                onMouseEnter={() => setIsLogoHovered(true)}
                onMouseLeave={() => setIsLogoHovered(false)}
              >
                <QuivrLogo
                  size={50}
                  color={
                    isLogoHovered ? "primary" : isDarkMode ? "white" : "black"
                  }
                />
              </div>

              <div className={styles.buttons_wrapper}>
                <div className={styles.block}>
                  <DiscussionButton />
                  <HomeButton />
                  <StudioButton />
                  <NotificationsButton />
                  <ThreadsButton />
                </div>
                <div className={styles.block}>
                  <UpgradeToPlusButton />
                  <ProfileButton />
                </div>
              </div>
              <div className={styles.social_buttons_wrapper}>
                <SocialsButtons />
              </div>
            </div>
          </AnimatedDiv>
        </div>
        <div
          className={`
        ${styles.menu_control_button_wrapper} 
        ${isOpened ? styles.shifted : ""}
        `}
        >
          <MenuControlButton />
        </div>
      </MotionConfig>
      {isVisible && (
        <div className={styles.notifications_panel}>
          <div className={styles.notifications_panel_header}>
            <span className={styles.title}>Notifications</span>
            <div className={styles.buttons}>
              <TextButton
                label="Mark all as read"
                color="black"
                onClick={() => void markAllAsRead()}
                disabled={unreadNotifications === 0}
              />
              <span>|</span>
              <TextButton
                label="Delete all"
                color="black"
                onClick={() => void deleteAllNotifications()}
                disabled={notifications.length === 0}
              />
            </div>
          </div>
          {notifications.length === 0 && (
            <div className={styles.no_notifications}>
              You have no notifications
            </div>
          )}
          {notifications.map((notification, i) => (
            <Notification
              key={i}
              notification={notification}
              lastNotification={i === notifications.length - 1}
              updateNotifications={updateNotifications}
            />
          ))}
        </div>
      )}
    </div>
  );
};
