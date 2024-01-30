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
import { BrainsManagementButton } from "./components/BrainsManagementButton/BrainsManagementButton";
import { DiscussionButton } from "./components/DiscussionButton/DiscussionButton";
import { HistoryButton } from "./components/HistoryButton/HistoryButton";
import { HomeButton } from "./components/HomeButton/HomeButton";

export const Menu = (): JSX.Element => {
  const { isOpened } = useMenuContext();
  const router = useRouter();
  const pathname = usePathname() ?? "";
  const [isLogoHovered, setIsLogoHovered] = useState<boolean>(false);

  useChatsList();

  if (nonProtectedPaths.includes(pathname)) {
    return <></>;
  }

  const displayedOnPages = [
    "/chat",
    "/library",
    "/brains-management",
    "/search",
  ];

  const isMenuDisplayed = displayedOnPages.some((page) =>
    pathname.includes(page)
  );

  if (!isMenuDisplayed) {
    return <></>;
  }

  /* eslint-disable @typescript-eslint/restrict-template-expressions */

  return (
    <MotionConfig transition={{ mass: 1, damping: 10, duration: 0.1 }}>
      <div className={styles.menu_container}>
        <AnimatedDiv>
          <div className="flex flex-col flex-1 p-4 gap-4 h-full">
            <div
              className={styles.quivr_logo_wrapper}
              onClick={() => router.push("/search")}
              onMouseEnter={() => setIsLogoHovered(true)}
              onMouseLeave={() => setIsLogoHovered(false)}
            >
              <QuivrLogo size={60} color={isLogoHovered ? "accent" : "white"} />
            </div>
            <div className="flex flex-1 w-full">
              <div className="w-full gap-2 flex flex-col">
                <DiscussionButton />
                <HomeButton />
                <BrainsManagementButton />
                <HistoryButton />
              </div>
            </div>
            {/* <div>
              <UpgradeToPlus />
              <ProfileButton />
            </div> */}
          </div>
        </AnimatedDiv>
      </div>
      <div
        className={`${styles.menu_control_button_wrapper} ${
          isOpened ? styles.shifted : ""
        }`}
      >
        <MenuControlButton />
      </div>
    </MotionConfig>
  );
};
