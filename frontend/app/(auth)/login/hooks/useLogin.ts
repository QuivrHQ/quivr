import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useLogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isPending, setIsPending] = useState(false);
  const { publish } = useToast();
  const { supabase, session } = useSupabase();

  const { track } = useEventTracking();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { t } = useTranslation(["login"]);

  const handleLogin = async () => {
    setIsPending(true);
    const { error } = await supabase.auth.signInWithPassword({
      email: email,
      password: password,
    });
    if (error) {
      console.log(error.message)
      if (error.message.includes("Failed")) {
        publish({
          variant: "danger",
          text: t("Failedtofetch",{ ns: 'login' })
        });
      } else if (error.message.includes("Invalid")) {
        publish({
          variant: "danger",
          text: t("Invalidlogincredentials",{ ns: 'login' })
        });
      } else {
        publish({
          variant: "danger",
          // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-call
          text: error.message
        });
      }
    } else {
      publish({
        variant: "success",
        text: t("loginSuccess",{ ns: 'login' })
      });
    }
    setIsPending(false);
  };

  useEffect(() => {
    if (session?.user !== undefined) {
      void track("SIGNED_IN");

      const previousPage = sessionStorage.getItem("previous-page");
      if (previousPage === null) {
        redirect("/upload");
      } else {
        sessionStorage.removeItem("previous-page");
        redirect(previousPage);
      }
    }
  }, [session?.user]);

  return {
    handleLogin,
    setEmail,
    setPassword,
    email,
    isPending,
    password,
  };
};
