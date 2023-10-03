"use client";

import { usePathname } from "next/navigation";

import { Header } from "./components/Header";
import { Logo } from "./components/Logo";
import { MobileMenu } from "./components/MobileMenu";
import { NavItems } from "./components/NavItems";

export const NavBar = (): JSX.Element => {
  const path = usePathname();
  const pageHasSidebar =
    path === null ||
    path.startsWith("/chat") ||
    path.startsWith("/brains-management");

  if (pageHasSidebar) {
    return <></>;
  }

  return (
    <Header>
      <Logo />
      <NavItems className="hidden sm:flex" />
      <MobileMenu />
    </Header>
  );
};
