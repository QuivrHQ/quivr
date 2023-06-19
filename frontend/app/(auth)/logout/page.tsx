/* eslint-disable */
"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { useSupabase } from "@/app/supabase-provider";
import Button from "@/lib/components/ui/Button";
import Card from "@/lib/components/ui/Card";
import PageHeading from "@/lib/components/ui/PageHeading";
import { useToast } from "@/lib/hooks/useToast";

export default function Logout() {
  const { supabase } = useSupabase();
  const [isPending, setIsPending] = useState(false);

  const { publish } = useToast();
  const router = useRouter();

  const handleLogout = async () => {
    setIsPending(true);
    const { error } = await supabase.auth.signOut();

    if (error) {
      console.error("Error logging out:", error.message);
      publish({
        variant: "danger",
        text: `Error logging out: ${error.message}`,
      });
    } else {
      publish({
        variant: "success",
        text: "Logged out successfully",
      });
      router.replace("/");
    }
    setIsPending(false);
  };

  return (
    <main>
      <section className="w-full min-h-[80vh] h-full outline-none flex flex-col gap-5 items-center justify-center p-6">
        <PageHeading title="Logout" subtitle="See you next time" />
        <Card className="max-w-md w-full p-5 sm:p-10 text-center flex flex-col items-center gap-5">
          <h2 className="text-lg">Are you sure you want to sign out?</h2>
          <div className="flex gap-5 items-center justify-center">
            <Link href={"/"}>
              <Button variant={"primary"}>Go back</Button>
            </Link>
            <Button
              isLoading={isPending}
              variant={"danger"}
              onClick={() => handleLogout()}
            >
              Log Out
            </Button>
          </div>
        </Card>
      </section>
    </main>
  );
}
