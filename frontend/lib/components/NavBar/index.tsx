"use client";

import { Header } from "./components/Header";
import { Logo } from "./components/Logo";
import { MobileMenu } from "./components/MobileMenu";
import { NavItems } from "./components/NavItems";

export const NavBar = (): JSX.Element => {
  return (
    <Header>
      <Logo />
      <NavItems className="hidden sm:flex" />
      <MobileMenu />
    </Header>
  );
};
