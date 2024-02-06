import { MotionConfig } from "framer-motion";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";

import { MenuControlButton } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/MenuControlButton/MenuControlButton";
import { useChatsList } from "@/app/chat/[chatId]/hooks/useChatsList";
import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { nonProtectedPaths } from "@/lib/config/routesConfig";
import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";

import styles from "./Menu.module.scss";
import { AnimatedDiv } from "./components/AnimationDiv";
import { DiscussionButton } from "./components/DiscussionButton/DiscussionButton";
import { HistoryButton } from "./components/HistoryButton/HistoryButton";
import { HomeButton } from "./components/HomeButton/HomeButton";
import { ProfileButton } from "./components/ProfileButton/ProfileButton";
import { StudioButton } from "./components/StudioButton/StudioButton";
import { UpgradeToPlusButton } from "./components/UpgradeToPlusButton/UpgradeToPlusButton";

export const Menu = (): JSX.Element => {
  const { isOpened } = useMenuContext();
  const router = useRouter();
  const pathname = usePathname() ?? "";
  const [isLogoHovered, setIsLogoHovered] = useState<boolean>(false);

  useChatsList();

  if (nonProtectedPaths.includes(pathname)) {
    return <></>;
  }

  const displayedOnPages = ["/chat", "/library", "/studio", "/search", "/user"];

  const isMenuDisplayed = displayedOnPages.some((page) =>
    pathname.includes(page)
  );

  if (!isMenuDisplayed) {
    return <></>;
  }

  return (
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
                color={isLogoHovered ? "primary" : "black"}
              />
            </div>

            <div className={styles.buttons_wrapper}>
              <div className={styles.block}>
                <DiscussionButton />
                <HomeButton />
                <StudioButton />
                <HistoryButton />
              </div>
              <div className={styles.block}>
                <UpgradeToPlusButton />
                <ProfileButton />
              </div>
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
  );
};
