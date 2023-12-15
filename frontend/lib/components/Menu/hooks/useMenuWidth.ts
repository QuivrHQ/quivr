import { usePathname } from "next/navigation";

import { useDevice } from "@/lib/hooks/useDevice";

const OPENED_MENU_WIDTH = 260;

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMenuWidth = () => {
  const pathname = usePathname() ?? "";
  const { isMobile } = useDevice();

  const rightSideBarActivated = !isMobile && pathname.includes("/chat");

  const isStaticSideBarActivated = !isMobile || !pathname.includes("/chat");

  const menuWidth = isStaticSideBarActivated ? OPENED_MENU_WIDTH : 0;

  return {
    OPENED_MENU_WIDTH,
    menuWidth,
    rightSideBarWidth: rightSideBarActivated ? OPENED_MENU_WIDTH : 0,
  };
};
