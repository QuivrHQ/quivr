"use client";
import { useEffect, useRef, useState } from "react";
import Card from "../components/ui/Card";
import PageHeading from "../components/ui/PageHeading";
import { useSupabase } from "../supabase-provider";
import Button from "../components/ui/Button";
import Link from "next/link";
import Toast, { ToastRef } from "../components/ui/Toast";

export default function Logout() {
  const { supabase } = useSupabase();
  const [isPending, setIsPending] = useState(false);

  const logoutToast = useRef<ToastRef>(null);
  const logoutErrorToast = useRef<ToastRef>(null);
  const [error, setError] = useState("Unknown Error");

  const handleLogout = async () => {
    setIsPending(true);
    const { error } = await supabase.auth.signOut();

    if (error) {
      console.error("Error logging out:", error.message);
      setError(error.message);
      logoutErrorToast.current?.publish();
    } else {
      console.log("User logged out");
      logoutToast.current?.publish();
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
      <Toast variant="danger" ref={logoutErrorToast}>
        {error}
      </Toast>
    </main>
  );
}
