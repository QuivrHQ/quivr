import { MotionConfig } from "framer-motion";
import { usePathname } from "next/navigation";

import { nonProtectedPaths } from "@/lib/config/routesConfig";

import { AnimatedDiv } from "./components/AnimationDiv";
import { BrainsManagementButton } from "./components/BrainsManagementButton";
import { DiscussionButton } from "./components/DiscussionButton";
import { ExplorerButton } from "./components/ExplorerButton";
import { MenuHeader } from "./components/MenuHeader";
import { ParametersButton } from "./components/ParametersButton";
import { ProfileButton } from "./components/ProfileButton";
import { UpgradeToPlus } from "./components/UpgradeToPlus";

export const Menu = (): JSX.Element => {
  const pathname = usePathname() ?? "";

  if (nonProtectedPaths.includes(pathname)) {
    return <></>;
  }

  const isChatPage = pathname.includes("/chat");

  if (!isChatPage) {
    return <></>;
  }

  return (
    <MotionConfig transition={{ mass: 1, damping: 10, duration: 0.2 }}>
      <div className="flex flex-col fixed sm:sticky top-0 left-0 h-full overflow-visible z-30 border-r border-black/10 dark:border-white/25 bg-white dark:bg-black">
        <AnimatedDiv>
          <div className="flex flex-col flex-1 p-4 gap-4">
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
    </MotionConfig>
  );
};
