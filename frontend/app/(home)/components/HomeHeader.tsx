import * as Popover from "@radix-ui/react-popover";
import Link from "next/link";
import { useTranslation } from "react-i18next";
import { AiFillStar } from "react-icons/ai";
import { LuChevronRight, LuMenu, LuX } from "react-icons/lu";

import { QuivrLogo } from "./QuivrLogo";

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
        className="flex justify-between items-center hover:text-primary p-2 md:text-white md:hover:text-gray-200 gap-1"
      >
        {leftIcon}
        {label}
        <LuChevronRight size={16} className={leftIcon ? "md:hidden" : ""} />
      </Link>
    </li>
  ));

  return (
    <header className="w-screen flex justify-between items-center p-5 min-w-max md:max-w-4xl m-auto">
      <div className="text-white text-3xl flex gap-2 items-center">
        <QuivrLogo size={64} />
        <div className="cursor-default">Quivr</div>
      </div>
      <div className="hidden md:flex">
        <ul className="flex gap-4 items-center">{navLinks}</ul>
      </div>
      <div className="md:hidden">
        <Popover.Root>
          <div>
            <Popover.Anchor />
            <Popover.Trigger>
              <button
                title="menu"
                type="button"
                className="text-white bg-[#D9D9D9] bg-opacity-30 rounded-full px-4 py-1"
              >
                <LuMenu size={32} />
              </button>
            </Popover.Trigger>
          </div>
          <Popover.Content
            style={{
              minWidth: "max-content",
              backgroundColor: "white",
              borderRadius: "0.75rem",
              paddingTop: "0.5rem",
              paddingInline: "1rem",
              paddingBottom: "1.5rem",
              marginRight: "1rem",
              marginTop: "-1rem",
            }}
          >
            <div className="flex flex-col gap-4 min-w-max w-[calc(100vw-4rem)] sm:w-[300px]">
              <div className="flex justify-between items-center">
                <div className="flex gap-2 items-center">
                  <QuivrLogo size={64} color="primary" />
                  <div className="text-lg font-medium text-primary cursor-default ">
                    Quivr
                  </div>
                </div>
                <Popover.Close>
                  <button
                    title="close"
                    type="button"
                    className="hover:text-primary p-2"
                  >
                    <LuX size={24} />
                  </button>
                </Popover.Close>
              </div>
              <nav>
                <ul className="flex flex-col bg-[#F5F8FF] rounded-xl p-2">
                  {navLinks}
                </ul>
              </nav>
            </div>
          </Popover.Content>
        </Popover.Root>
      </div>
    </header>
  );
};
