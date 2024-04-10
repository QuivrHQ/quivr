"use client";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import styles from "./page.module.scss";

const Search = (): JSX.Element => {
  const pathname = usePathname();
  const { session } = useSupabase();

  useEffect(() => {
    if (session === null) {
      redirectToLogin();
    }
  }, [pathname, session]);

  return (
    <div className={styles.page_header}>
      <PageHeader iconName="assistant" label="Quivr Assistants" buttons={[]} />
    </div>
  );
};

export default Search;
