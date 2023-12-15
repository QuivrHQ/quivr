import { usePathname } from "next/navigation";

import { useSideBarContext } from "@/lib/context/SidebarProvider/hooks/useSideBarContext";
import { useDevice } from "@/lib/hooks/useDevice";

const OPENED_MENU_WIDTH = 260;

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMenuWidth = () => {
  const pathname = usePathname() ?? "";
  const { isOpened } = useSideBarContext();
  const { isMobile } = useDevice();

  const shouldDisplayRightSideBar = !isMobile && pathname.includes("/chat");

  const shouldSideBarBeSticky =
    (!isMobile && pathname.includes("/chat")) || isOpened;

  return {
    OPENED_MENU_WIDTH,
    shouldDisplayRightSideBar,
    shouldSideBarBeSticky,
  };
};
