/* eslint-disable */
"use client";
import Link from "next/link";

import Button from "@/lib/components/ui/Button";
import Card from "@/lib/components/ui/Card";
import PageHeading from "@/lib/components/ui/PageHeading";
import { useLogout } from "./hooks/useLogout";

export default function Logout() {
  const { handleLogout, isPending } = useLogout();
  return (
    <main data-testid="logout-page">
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
              data-testid="logout-button"
            >
              Log Out
            </Button>
          </div>
        </Card>
      </section>
    </main>
  );
}
