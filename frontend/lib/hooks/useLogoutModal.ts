import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useLogoutModal = () => {
  const { supabase } = useSupabase();
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [isLogoutModalOpened, setIsLogoutModalOpened] = useState(false);
  const { track } = useEventTracking();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { t } = useTranslation(["translation", "logout"]);

  const { publish } = useToast();

  const handleLogout = async () => {
    setIsLoggingOut(true);
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
      window.location.href = "/";
    }
    setIsLoggingOut(false);
  };

  return {
    handleLogout,
    isLoggingOut,
    isLogoutModalOpened,
    setIsLogoutModalOpened,
  };
};
