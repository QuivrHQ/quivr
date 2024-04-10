"use client";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

const Search = (): JSX.Element => {
  const pathname = usePathname();
  const { session } = useSupabase();

  useEffect(() => {
    if (session === null) {
      redirectToLogin();
    }
  }, [pathname, session]);

  return <>Assistants</>;
};

export default Search;
