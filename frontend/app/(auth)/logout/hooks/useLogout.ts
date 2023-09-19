import { useRouter } from "next/navigation";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useLogout = () => {
  const { supabase } = useSupabase();
  const [isPending, setIsPending] = useState(false);
  const { track } = useEventTracking();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { t, i18n } = useTranslation(["translation", "logout"]);

  const { publish } = useToast();
  const router = useRouter();

  const handleLogout = async () => {
    setIsPending(true);
    const { error } = await supabase.auth.signOut();
    void track("LOGOUT");
    localStorage.clear();

    if (error) {
      console.error("Error logging out:", error.message);
      publish({
        variant: "danger",
        text: t("error", { errorMessage: error.message, ns: "logout" }),
      });
    } else {
      publish({
        variant: "success",
        text: t("loggedOut", { ns: "logout" }),
      });
      router.replace("/");
    }
    setIsPending(false);
  };

  return {
    handleLogout,
    isPending,
  };
};
