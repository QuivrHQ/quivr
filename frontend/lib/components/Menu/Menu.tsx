import { MotionConfig } from "framer-motion";
import { usePathname } from "next/navigation";

import { MenuControlButton } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/MenuControlButton/MenuControlButton";
import { nonProtectedPaths } from "@/lib/config/routesConfig";
import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";

import styles from "./Menu.module.scss";
import { AnimatedDiv } from "./components/AnimationDiv";
import { BrainsManagementButton } from "./components/BrainsManagementButton";
import { DiscussionButton } from "./components/DiscussionButton/DiscussionButton";
import { MenuHeader } from "./components/MenuHeader";
import { ProfileButton } from "./components/ProfileButton";
import { UpgradeToPlus } from "./components/UpgradeToPlus";

export const Menu = (): JSX.Element => {
  const { isOpened } = useMenuContext();
  const pathname = usePathname() ?? "";

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
    <MotionConfig transition={{ mass: 1, damping: 10, duration: 0.2 }}>
      <div className="flex flex-col fixed sm:sticky top-0 left-0 h-full overflow-visible z-[1000] border-r border-black/10 dark:border-white/25 bg-highlight">
        <AnimatedDiv>
          <div className="flex flex-col flex-1 p-4 gap-4 h-full">
            <MenuHeader />
            <div className="flex flex-1 w-full">
              <div className="w-full gap-2 flex flex-col">
                <DiscussionButton />
                <BrainsManagementButton />
              </div>
            </div>
            <div>
              <UpgradeToPlus />
              <ProfileButton />
            </div>
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
