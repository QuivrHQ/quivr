import { usePathname } from "next/navigation";

import { useDevice } from "@/lib/hooks/useDevice";

const OPENED_MENU_WIDTH = 260;

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMenuWidth = () => {
  const pathname = usePathname() ?? "";
  const { isMobile } = useDevice();

  const isStaticSideBarActivated = !isMobile;

  const shouldAddFixedPadding = pathname.startsWith("/chat");

  const staticMenuWidth =
    shouldAddFixedPadding && isStaticSideBarActivated ? OPENED_MENU_WIDTH : 0;

  return {
    OPENED_MENU_WIDTH,
    staticMenuWidth,
  };
};
