"use client";
import { redirect } from "next/navigation";

import { useSupabase } from "../supabase-provider";
import { ConfigForm, ConfigTitle } from "./components";

// TODO: Use states instead of NEXTJS router to open and close modal
export default function ConfigPage() {
  const { session } = useSupabase();

  if (session === null) {
    redirect("/login");
  }

  return (
    <main className="w-full flex flex-col">
      <section className="w-full outline-none pt-10 flex flex-col gap-5 items-center justify-center p-6">
        <ConfigTitle />
        <ConfigForm />
      </section>
    </main>
  );
}
