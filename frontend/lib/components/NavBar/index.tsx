"use client";

import { usePathname } from "next/navigation";

import { Header } from "./components/Header";
import { Logo } from "./components/Logo";
import { MobileMenu } from "./components/MobileMenu";
import { NavItems } from "./components/NavItems";

export const NavBar = (): JSX.Element => {
  const path = usePathname();

  return (
    <>
      {path === null || path.startsWith("/chat") ? (
        <></>
      ) : (
        <Header>
          <Logo />
          <NavItems className="hidden sm:flex" />
          <MobileMenu />
        </Header>
      )}
    </>
  );
};
