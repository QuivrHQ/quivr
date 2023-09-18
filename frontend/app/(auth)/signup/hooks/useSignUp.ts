import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks/useToast";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSignUp = () => {
  const { supabase } = useSupabase();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isPending, setIsPending] = useState(false);
  const { track } = useEventTracking();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { t } = useTranslation(["signUp"]);

  const { publish } = useToast();
  const handleSignUp = async () => {
    void track("SIGNUP");
    setIsPending(true);
    const { error } = await supabase.auth.signUp({
      email: email,
      password: password,
    });

    if (error) {
      console.error("Error signing up:", error.message);
      publish({
        variant: "danger",
        text: t("errorSignUp", { errorMessage: error.message }),
      });
    } else {
      publish({
        variant: "success",
        text: t("mailSended"),
      });
    }
    setIsPending(false);
  };

  return {
    handleSignUp,
    setEmail,
    password,
    setPassword,
    isPending,
    email,
  };
};
