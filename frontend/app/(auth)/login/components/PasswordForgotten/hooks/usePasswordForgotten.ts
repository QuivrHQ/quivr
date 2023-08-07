import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";

type UsePasswordForgottenProps = {
  email: string;
  setEmail: (email: string) => void;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePasswordForgotten = ({
  email,
  setEmail,
}: UsePasswordForgottenProps) => {
  const [isPending, setIsPending] = useState(false);
  const { supabase } = useSupabase();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const {t, i18n} = useTranslation(["login"]);

  const { publish } = useToast();

  const handleRecoverPassword = async () => {
    if (email === "") {
      publish({
        variant: "danger",
        text: t("errorMailMissed",{ ns: 'login' })
      });

      return;
    }

    setIsPending(true);

    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/recover-password`,
    });

    if (error) {
      publish({
        variant: "danger",
        text: error.message,
      });
    } else {
      publish({
        variant: "success",
        text: t("recoveryMailSended",{ ns: 'login' })
      });

      setEmail("");
    }
    setIsPending(false);
  };

  return {
    isPending,
    handleRecoverPassword,
  };
};
