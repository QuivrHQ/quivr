"use client";

import { usePathname } from "next/navigation";
import { useEffect } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { useJune } from "./useJune";

export const usePageTracking = (): void => {
  const analytics = useJune();
  const pathname = usePathname();
  const { session } = useSupabase();

  useEffect(() => {
    if (pathname !== null) {
      const handleRouteChange = async () => {
        await analytics?.identify(session?.user.id);
        await analytics?.page(pathname);
      };

      void handleRouteChange();
    }
  }, [analytics, pathname, session?.user.id]);
};
