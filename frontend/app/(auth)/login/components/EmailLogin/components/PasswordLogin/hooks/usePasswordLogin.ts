import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { EmailAuthContextType } from "@/app/(auth)/login/types";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePasswordLogin = () => {
  const { supabase } = useSupabase();
  const { t } = useTranslation("login");
  const { publish } = useToast();
  const { watch, setValue } = useFormContext<EmailAuthContextType>();

  const email = watch("email");
  const password = watch("password");

  const handlePasswordLogin = async () => {
    if (email === "") {
      publish({
        variant: "danger",
        text: t("errorMailMissed"),
      });

      return;
    }

    if (password === "") {
      publish({
        variant: "danger",
        text: t("errorPasswordMissed"),
      });

      return;
    }
    setValue("isPasswordSubmitting", true);
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    setValue("isPasswordSubmitting", false);
    setValue("isPasswordSubmitted", true);

    if (error) {
      publish({
        variant: "danger",
        text: error.message,
      });

      throw error; // this error is caught by react-hook-form
    }
  };

  return {
    handlePasswordLogin,
  };
};
