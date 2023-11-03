"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";

export const useSecurity = (): {
  isStudioMember: boolean;
  isPageAccessOk: boolean;
} => {
  const [isStudioMember, setIsStudioMember] = useState<boolean>(false);

  const { session } = useSupabase();
  const path = usePathname();

  const securityPages = ["/login", "/chat", "/share", "/user"];
  const isPageAccessOk =
    path === "/" ||
    securityPages.some((page: string) => path?.startsWith(page));

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
    if (session?.user.email) {
      setIsStudioMember(session.user.email.indexOf("@stayreal.studio") !== -1);
    }
  }, [session?.user.email]);

  return { isStudioMember, isPageAccessOk };
};
