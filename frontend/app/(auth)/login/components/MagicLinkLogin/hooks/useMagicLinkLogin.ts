import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMagicLinkLogin = () => {
  const { supabase } = useSupabase();
  const { t } = useTranslation("login");
  const { publish } = useToast();

  const {
    register,
    watch,
    setValue,
    formState: { isSubmitSuccessful, isSubmitting },
    handleSubmit,
    reset,
  } = useForm<{ email: string }>({
    defaultValues: {
      email: "",
    },
  });

  const email = watch("email");

  const handleMagicLinkLogin = handleSubmit(async (_, ev) => {
    ev?.preventDefault();
    if (email === "") {
      publish({
        variant: "danger",
        text: t("errorMailMissed"),
      });

      return;
    }

    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: window.location.hostname, // current domain name. for eg localhost:3000, localhost:3001, https://...
      },
    });

    if (error) {
      publish({
        variant: "danger",
        text: error.message,
      });

      throw error; // this error is caught by react-hook-form
    }

    setValue("email", "");
  });

  return {
    handleMagicLinkLogin,
    isSubmitting,
    register,
    handleSubmit,
    isSubmitSuccessful,
    reset,
  };
};
