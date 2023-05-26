"use client";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { useSupabase } from "@/app/supabase-provider";
import Toast, { ToastRef } from "@/app/components/ui/Toast";
import PageHeading from "@/app/components/ui/PageHeading";
import Button from "@/app/components/ui/Button";
import Card from "@/app/components/ui/Card";
import Link from "next/link";

export default function Logout() {
  const { supabase } = useSupabase();
  const [isPending, setIsPending] = useState(false);

  const logoutToast = useRef<ToastRef>(null);
  const [error, setError] = useState("Unknown Error");

  const router = useRouter();

  const handleLogout = async () => {
    setIsPending(true);
    const { error } = await supabase.auth.signOut();

    if (error) {
      console.error("Error logging out:", error.message);
      setError(error.message);
      logoutToast.current?.publish({
        variant: "danger",
        text: `Error logging out: ${error.message}`,
      });
    } else {
      console.log("User logged out");
      logoutToast.current?.publish({
        variant: "success",
        text: "Logged out successfully",
      });
      router.replace("/");
    }
    setIsPending(false);
  };

  // useEffect(() => {
  //   handleLogout();
  // }, []);

  return (
    <main>
      <section className="w-full min-h-screen h-full outline-none flex flex-col gap-5 items-center justify-center p-6">
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
      <Toast variant="success" ref={logoutToast}>
        Logged Out Successfully
      </Toast>
      <Toast variant="danger" ref={logoutToast}>
        {error}
      </Toast>
    </main>
  );
}
