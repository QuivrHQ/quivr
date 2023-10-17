import Link from "next/link";
import { useTranslation } from "react-i18next";
import { AiFillStar } from "react-icons/ai";
import { LuChevronRight } from "react-icons/lu";

import { HomeHeaderBackground } from "./components/HomeHeaderBackground";
import { PopoverMenuMobile } from "./components/PopoverMenuMobile";
import { QuivrLogo } from "./components/QuivrLogo";

export const HomeHeader = (): JSX.Element => {
  const { t } = useTranslation("home");

  const navItems = [
    {
      href: "https://github.com/StanGirard/quivr",
      label: t("star_us"),
      leftIcon: <AiFillStar size={16} className="hidden md:inline" />,
    },
    { href: "/signup", label: t("sign_up") },
    { href: "/login", label: t("sign_in") },
  ];

  const navLinks = navItems.map(({ href, label, leftIcon }) => (
    <li key={label}>
      <Link
        href={href}
        className="flex justify-between items-center hover:text-primary p-2 md:text-white md:hover:text-slate-200 gap-1"
      >
        {leftIcon}
        {label}
        <LuChevronRight size={16} className={leftIcon ? "md:hidden" : ""} />
      </Link>
    </li>
  ));

  return (
    <>
      <HomeHeaderBackground />
      <header className="w-screen flex justify-between items-center p-5 min-w-max md:max-w-6xl m-auto">
        <div className="text-white text-3xl flex gap-2 items-center">
          <QuivrLogo size={64} />
          <div className="cursor-default">Quivr</div>
        </div>
        <div className="hidden md:flex">
          <ul className="flex gap-4 items-center">{navLinks}</ul>
        </div>
        <div className="md:hidden z-[1]">
          <PopoverMenuMobile navLinks={navLinks} />
        </div>
      </header>
    </>
  );
};
