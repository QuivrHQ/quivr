import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { EmailAuthContextType } from "@/app/(auth)/login/types";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMagicLinkLogin = () => {
  const { supabase } = useSupabase();
  const { watch, setValue } = useFormContext<EmailAuthContextType>();

  const { t } = useTranslation("login");
  const { publish } = useToast();

  const email = watch("email");

  const handleMagicLinkLogin = async () => {
    if (email === "") {
      publish({
        variant: "danger",
        text: t("errorMailMissed"),
      });

      return;
    }
    setValue("isMagicLinkSubmitting", true);
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: window.location.hostname,
      },
    });
    setValue("isMagicLinkSubmitting", false);
    setValue("isMagicLinkSubmitted", true);

    if (error) {
      publish({
        variant: "danger",
        text: error.message,
      });

      throw error;
    }
  };

  return {
    handleMagicLinkLogin,
  };
};
