"use client";
import Button from "@/app/components/ui/Button";
import { useSupabase } from "@/app/supabase-provider";
import { useToast } from "@/lib/hooks/useToast";
import { useState } from "react";

type MaginLinkLoginProps = {
  email: string;
  setEmail: (email: string) => void;
};

export const MagicLinkLogin = ({ email, setEmail }: MaginLinkLoginProps) => {
  const { supabase } = useSupabase();
  const [isPending, setIsPending] = useState(false);

  const { publish } = useToast();

  const handleLogin = async () => {
    if (email === "") {
      publish({
        variant: "danger",
        text: "Please enter your email address",
      });
      return;
    }

    setIsPending(true);

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
    } else {
      publish({
        variant: "success",
        text: "Magic link sent successfully if email recognized",
      });

      setEmail("");
    }
    setIsPending(false);
  };

  return (
    <Button
      type="button"
      variant={"tertiary"}
      onClick={handleLogin}
      isLoading={isPending}
    >
      Send Magic Link
    </Button>
  );
};
