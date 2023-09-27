"use client";
import { Dispatch, HTMLAttributes, SetStateAction } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { cn } from "@/lib/utils";

import { AuthButtons } from "./components/AuthButtons";
import { NavLink } from "./components/NavLink";

interface NavItemsProps extends HTMLAttributes<HTMLUListElement> {
  setOpen?: Dispatch<SetStateAction<boolean>>;
}

export const NavItems = ({
  className,
  setOpen,
  ...props
}: NavItemsProps): JSX.Element => {
  const { session } = useSupabase();
  const isUserLoggedIn = session?.user !== undefined;

  return (
    <ul
      className={cn(
        "flex flex-row items-center gap-4 text-sm flex-1",
        className
      )}
      {...props}
    >
      {!isUserLoggedIn && (
        <>
          <NavLink setOpen={setOpen} to="https://github.com/StanGirard/quivr">
            Github
          </NavLink>
          <NavLink setOpen={setOpen} to="https://discord.gg/HUpRgp2HG8">
            Discord
          </NavLink>
        </>
      )}
      <div className="flex sm:flex-1 sm:justify-end flex-row items-center justify-center sm:flex-row gap-5 sm:gap-2">
        {!isUserLoggedIn && <AuthButtons />}
      </div>
    </ul>
  );
};
