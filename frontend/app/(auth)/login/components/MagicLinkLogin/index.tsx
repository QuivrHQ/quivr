"use client";
import Button from "@/app/components/ui/Button";
import Toast from "@/app/components/ui/Toast";
import { useToast } from "@/app/hooks/useToast";
import { useSupabase } from "@/app/supabase-provider";
import { useState } from "react";

type MaginLinkLoginProps = {
  email: string;
  setEmail: (email: string) => void;
};

export const MagicLinkLogin = ({ email, setEmail }: MaginLinkLoginProps) => {
  const { supabase } = useSupabase();
  const [isPending, setIsPending] = useState(false);

  const { setMessage, messageToast } = useToast();

  const handleLogin = async () => {
    if (email === "") {
      setMessage({
        type: "error",
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
      setMessage({
        type: "danger",
        text: error.message,
      });
    } else {
      setMessage({
        type: "success",
        text: "Magic link sent successfully if email recognized",
      });

      setEmail("");
    }
    setIsPending(false);
  };

  return (
    <>
      <Button
        type="button"
        variant={"tertiary"}
        onClick={handleLogin}
        isLoading={isPending}
      >
        Send Magic Link
      </Button>
      <Toast ref={messageToast} />
    </>
  );
};
