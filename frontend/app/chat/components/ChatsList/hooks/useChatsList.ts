import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { useDevice } from "@/lib/hooks/useDevice";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatsList = () => {
  const { isMobile } = useDevice();

  const [open, setOpen] = useState(!isMobile);

  const pathname = usePathname();

  useEffect(() => {
    setOpen(!isMobile);
  }, [isMobile]);

  useEffect(() => {
    setOpen(!isMobile);
  }, [isMobile, pathname]);

  return {
    open,
    setOpen,
  };
};
