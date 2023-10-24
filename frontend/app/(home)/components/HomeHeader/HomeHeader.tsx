import Link from "next/link";
import { useTranslation } from "react-i18next";
import { AiFillStar } from "react-icons/ai";
import { LuChevronRight } from "react-icons/lu";

import { cn } from "@/lib/utils";

import { PopoverMenuMobile } from "./components/PopoverMenuMobile";
import { QuivrLogo } from "./components/QuivrLogo";
import { NavbarItem } from "./types";

type HomeNavProps = {
  color?: "white" | "black";
};

export const HomeHeader = ({ color = "white" }: HomeNavProps): JSX.Element => {
  const { t } = useTranslation("home");
  const linkStyle = {
    white: "text-white hover:text-slate-200",
    black: "text-black",
  };

  const navItems: NavbarItem[] = [
    {
      href: "https://theodo.co.uk",
      label: `${t("sponsored_by")} Theodo`,
      rightIcon: null,
      newTab: true,
      className: "underline",
    },
    {
      href: "https://github.com/StanGirard/quivr",
      label: t("star_us"),
      leftIcon: <AiFillStar size={16} className="hidden md:inline" />,
      rightIcon: null,
    },
    { href: "/blog", label: t("blog"), rightIcon: null, newTab: true },
    { href: "/signup", label: t("sign_up") },
    { href: "/login", label: t("sign_in") },
  ];

  const navLinks = (device: "mobile" | "desktop") =>
    navItems.map(
      ({ href, label, leftIcon, rightIcon, newTab = false, className }) => (
        <li key={label}>
          <Link
            href={href}
            {...(newTab && { target: "_blank", rel: "noopener noreferrer" })}
            className={cn(
              "flex justify-between items-center hover:text-primary p-2 gap-1",
              device === "desktop" ? linkStyle[color] : null,
              className
            )}
          >
            {leftIcon}
            {label}
            {rightIcon !== null && (rightIcon ?? <LuChevronRight size={16} />)}
          </Link>
        </li>
      )
    );

  return (
    <header className="w-screen flex justify-between items-center p-5 min-w-max md:max-w-6xl m-auto">
      <Link
        href="/"
        className={cn(
          "text-3xl flex gap-2 items-center",
          linkStyle[color],
          color === "black" ? "hover:text-black" : "hover:text-white"
        )}
      >
        <QuivrLogo size={64} color={color} />
        <div>Quivr</div>
      </Link>
      <div className="hidden md:flex">
        <ul className="flex gap-4 items-center">{navLinks("desktop")}</ul>
      </div>
      <div className="md:hidden z-10">
        <PopoverMenuMobile navLinks={navLinks("mobile")} color={color} />
      </div>
    </header>
  );
};
