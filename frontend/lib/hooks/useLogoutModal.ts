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
    try {
      // Try to sign out normally
      const { error } = await supabase.auth.signOut();
      void track("LOGOUT");

      // Clear all storage - both localStorage and sessionStorage
      localStorage.clear();
      sessionStorage.clear();

      // Clear all cookies related to Supabase auth
      // eslint-disable-next-line prefer-arrow/prefer-arrow-functions
      document.cookie.split(";").forEach(function (c) {
        document.cookie = c
          .replace(/^ +/, "")
          .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
      });

      if (error) {
        // Log the error but continue with redirect
        console.error("Error logging out:", error.message);

        // If the error is related to invalid tokens, we can still proceed with logout
        if (
          error.message.includes("token") ||
          error.message.includes("session") ||
          error.message.includes("jwt")
        ) {
          console.log(
            "Session token error detected, proceeding with logout anyway"
          );
          // Force redirect to login page instead of home
          window.location.href = "/login";
        } else {
          // For other errors, show the toast
          publish({
            variant: "danger",
            text: t("error", { errorMessage: error.message, ns: "logout" }),
          });
        }
      } else {
        // Force redirect to login page instead of home
        window.location.href = "/login";
      }
    } catch (e) {
      // Catch any unexpected errors
      console.error("Unexpected error during logout:", e);
      localStorage.clear();
      sessionStorage.clear();
      // Force redirect to login page
      window.location.href = "/login";
    } finally {
      setIsLoggingOut(false);
    }
  };

  return {
    handleLogout,
    isLoggingOut,
    isLogoutModalOpened,
    setIsLogoutModalOpened,
  };
};
