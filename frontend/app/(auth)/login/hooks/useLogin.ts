import { useEffect, useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToPreviousPageOrChatPage } from "@/lib/helpers/redirectToPreviousPageOrChatPage";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useLogin = () => {
  const [email, setEmail] = useState("");

  const { session } = useSupabase();

  const { track } = useEventTracking();

  useEffect(() => {
    if (session?.user !== undefined) {
      void track("SIGNED_IN");
      redirectToPreviousPageOrChatPage();
    }
  }, [session?.user]);

  return {
    setEmail,
    email,
  };
};
