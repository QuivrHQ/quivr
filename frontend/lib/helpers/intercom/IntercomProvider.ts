import { usePathname } from "next/navigation";
import { useEffect } from "react";

import { useDevice } from "@/lib/hooks/useDevice";
import { useUserData } from "@/lib/hooks/useUserData";

import {
  boot as bootIntercom,
  load as loadIntercom,
  shutdown as shutdownIntercom,
  update as updateIntercom,
} from "./intercom";

export const IntercomProvider = ({
  children,
}: {
  children: React.ReactNode;
}): React.ReactNode => {
  const pathname = usePathname();
  const { userData } = useUserData();
  const { isMobile } = useDevice();

  if (
    typeof window !== "undefined" &&
    process.env.NEXT_PUBLIC_INTERCOM_APP_ID
  ) {
    if (isMobile && pathname?.includes("/chat")) {
      shutdownIntercom();
    } else {
      loadIntercom();
      bootIntercom(userData?.email ?? "");
    }
  }

  useEffect(() => {
    if (process.env.NEXT_PUBLIC_INTERCOM_APP_ID) {
      updateIntercom();
    }
  }, [pathname]);

  return children;
};
