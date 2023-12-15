import { MotionConfig } from "framer-motion";
import { usePathname } from "next/navigation";
import { LuPanelLeftOpen } from "react-icons/lu";

import { nonProtectedPaths } from "@/lib/config/routesConfig";
import { useSideBarContext } from "@/lib/context/SidebarProvider/hooks/useSideBarContext";

import { AnimatedDiv } from "./components/AnimationDiv";
import { BrainsManagementButton } from "./components/BrainsManagementButton";
import { DiscussionButton } from "./components/DiscussionButton";
import { ExplorerButton } from "./components/ExplorerButton";
import { MenuHeader } from "./components/MenuHeader";
import { ParametersButton } from "./components/ParametersButton";
import { ProfileButton } from "./components/ProfileButton";
import { UpgradeToPlus } from "./components/UpgradeToPlus";
import { useMenuWidth } from "./hooks/useMenuWidth";
import Button from "../ui/Button";

export const Menu = (): JSX.Element => {
  const pathname = usePathname() ?? "";

  const { setIsOpened } = useSideBarContext();

  const { shouldSideBarBeSticky, OPENED_MENU_WIDTH } = useMenuWidth();

  if (nonProtectedPaths.includes(pathname)) {
    return <></>;
  }

  const displayedOnPages = ["/chat", "/library"];

  const isMenuDisplayed = displayedOnPages.some((page) =>
    pathname.includes(page)
  );

  if (!isMenuDisplayed) {
    return <></>;
  }

  return (
    <MotionConfig transition={{ mass: 1, damping: 10, duration: 0.2 }}>
      <div
        className="flex flex-col fixed sm:sticky top-0 left-0 h-full overflow-visible z-[1000] border-r border-black/10 dark:border-white/25 bg-highlight"
        style={{
          width: shouldSideBarBeSticky ? OPENED_MENU_WIDTH : 0,
        }}
      >
        <AnimatedDiv>
          <div className="flex flex-col flex-1 p-4 gap-4 h-full">
            <MenuHeader />
            <div className="flex flex-1 w-full">
              <div className="w-full gap-2 flex flex-col">
                <DiscussionButton />
                <ExplorerButton />
                <BrainsManagementButton />
                <ParametersButton />
              </div>
            </div>
            <div>
              <UpgradeToPlus />
              <ProfileButton />
            </div>
          </div>
        </AnimatedDiv>
      </div>
      <Button
        variant="tertiary"
        onClick={() => setIsOpened((prev) => !prev)}
        className="absolute top-2 left-2 sm:hidden z-50"
      >
        <LuPanelLeftOpen className="text-primary" size={30} />
      </Button>
    </MotionConfig>
  );
};
