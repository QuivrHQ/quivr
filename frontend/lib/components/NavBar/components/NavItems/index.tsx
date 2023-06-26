"use client";
import { useFeature } from '@growthbook/growthbook-react';
import Link from "next/link";
import { Dispatch, HTMLAttributes, SetStateAction } from "react";
import { MdPerson, MdSettings } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { cn } from "@/lib/utils";

import { AuthButtons } from "./components/AuthButtons";
import { BrainsDropDown } from "./components/BrainsDropDown";
import { DarkModeToggle } from "./components/DarkModeToggle";
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
  const shouldUseMultipleBrains = useFeature('multiple-brains').on;
  
  return (
    <ul
      className={cn(
        "flex flex-row items-center gap-4 text-sm flex-1",
        className
      )}
      {...props}
    >
      {isUserLoggedIn ? (
        <>
          <NavLink setOpen={setOpen} to="/upload">
            上传
          </NavLink>
          <NavLink setOpen={setOpen} to="/chat">
            对话
          </NavLink>
          <NavLink setOpen={setOpen} to="/explore">
            查看
          </NavLink>
        </>
      ) : (
        <>
        {/*  <NavLink setOpen={setOpen} to="https://github.com/StanGirard/quivr">
            Github
          </NavLink>*/}
                      <NavLink setOpen={setOpen} to="https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=208ySzsw81s&businessType=9&from=181074&biz=ka&mainSourceId=share&subSourceId=others&jumpsource=shorturl#/out">
            QQ频道
          </NavLink> 
        </>
      )}
      <div className="flex sm:flex-1 sm:justify-end flex-col items-center justify-center sm:flex-row gap-5 sm:gap-2">
        {isUserLoggedIn && (
          <>
            {shouldUseMultipleBrains && (<BrainsDropDown />)}
            <Link aria-label="account" className="" href={"/user"}>
              <MdPerson className="text-2xl" />
            </Link>
            <Link href={"/config"}>
              <Button
                variant={"tertiary"}
                className="focus:outline-none text-2xl"
                aria-label="Settings"
              >
                <MdSettings />
              </Button>
            </Link>
          </>
        )}
        {!isUserLoggedIn && <AuthButtons />}

        <DarkModeToggle />
      </div>
    </ul>
  );
};
