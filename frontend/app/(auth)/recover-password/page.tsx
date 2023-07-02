/* eslint-disable */
"use client";
import { redirect, usePathname } from "next/navigation";
import { useState } from "react";

import Button from "@/lib/components/ui/Button";
import Card from "@/lib/components/ui/Card";
import Field from "@/lib/components/ui/Field";
import PageHeading from "@/lib/components/ui/PageHeading";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks/useToast";
import { useEventTracking } from "@/services/analytics/useEventTracking";

export default function RecoverPassword() {
  const { supabase, session } = useSupabase();
  const [password, setPassword] = useState("");
  const [isPending, setIsPending] = useState(false);
  const { track } = useEventTracking();
  const pathname = usePathname();
  const { publish } = useToast();
  const handleChangePassword = async () => {
    void track("UPDATE_PASSWORD");
    setIsPending(true);
    const { data, error } = await supabase.auth.updateUser({
      password: password,
    });

    if (error) {
      console.error("Error while resetting password:", error.message);
      publish({
        variant: "danger",
        text: `Error: ${error.message}`,
      });
    } else {
      publish({
        variant: "success",
        text: "Password updated successfully!",
      });
    }
    setIsPending(false);
  };

  if (session?.user === undefined) {
    redirect(`/login?previous-page=${pathname}`);
  }

  return (
    <main>
      <section className="min-h-[80vh] w-full h-full outline-none flex flex-col gap-5 items-center justify-center p-6">
        <PageHeading title="Update password" />
        <Card className="max-w-md w-full p-5 sm:p-10 text-left">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleChangePassword();
            }}
            className="flex flex-col gap-2"
          >
            <Field
              name="New password"
              required
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="New password"
              data-testid="password-field"
            />
            <div className="flex flex-col items-center justify-center mt-2 gap-2">
              <Button isLoading={isPending} data-testid="update-button">
                Update
              </Button>
            </div>
          </form>
        </Card>
      </section>
    </main>
  );
}
