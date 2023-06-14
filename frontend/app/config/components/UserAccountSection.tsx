/* eslint-disable */
"use client";

import Link from "next/link";

import { useSupabase } from "@/app/supabase-provider";
import Button from "@/lib/components/ui/Button";

export const UserAccountSection = (): JSX.Element => {
  const { session } = useSupabase();

  if (session === null) {
    return <></>;
  }

  return (
    <>
      <div className="border-b border-gray-300 mt-8 mb-8">
        <p className="text-center text-gray-600 uppercase tracking-wide font-semibold">
          Your Account
        </p>
      </div>
      <div className="flex justify-between items-center w-full">
        <span>
          Signed In as: <b>{session.user.email}</b>
        </span>
        <Link className="mt-2" href={"/logout"}>
          <Button className="px-3 py-2" variant={"danger"}>
            Logout
          </Button>
        </Link>
        {/* TODO: add functionality to change password */}
      </div>
    </>
  );
};
