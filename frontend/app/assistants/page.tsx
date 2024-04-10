"use client";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

import { useAssistants } from "@/lib/api/assistants/useAssistants";
import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import styles from "./page.module.scss";

const Search = (): JSX.Element => {
  const pathname = usePathname();
  const { session } = useSupabase();

  const { getAssistants } = useAssistants();

  useEffect(() => {
    if (session === null) {
      redirectToLogin();
    }

    void (async () => {
      try {
        const res = await getAssistants();
        console.info(res);
      } catch (error) {
        console.error(error);
      }
    })();
  }, [pathname, session]);

  return (
    <div className={styles.page_header}>
      <PageHeader iconName="assistant" label="Quivr Assistants" buttons={[]} />
    </div>
  );
};

export default Search;
