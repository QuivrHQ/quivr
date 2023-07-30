import { useRouter } from "next/navigation";
import { useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useLogout = () => {
  const { supabase } = useSupabase();
  const [isPending, setIsPending] = useState(false);
  const { track } = useEventTracking();

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
        text: `Error logging out: ${error.message}`,
      });
    } else {
      publish({
        variant: "success",
        text: "Logged out successfully",
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
