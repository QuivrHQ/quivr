import * as Popover from "@radix-ui/react-popover";
import Link from "next/link";
import { LuChevronRight, LuMenu, LuX } from "react-icons/lu";

import { QuivrLogo } from "./QuivrLogo";

export const HomeHeader = (): JSX.Element => {
  const navItems = [
    { href: "https://github.com/StanGirard/quivr", label: "Star us on GitHub" },
    { href: "/login", label: "Sign in" },
    { href: "/signup", label: "Sign up" },
  ];

  const navLinks = navItems.map(({ href, label }) => (
    <li key={label} className="flex justify-between hover:text-primary p-2">
      <Link href={href} className="">
        {label}
      </Link>
      <LuChevronRight size={16} />
    </li>
  ));

  return (
    <>
      <header className="w-screen flex justify-between items-center p-5 min-w-max">
        <div className="text-white text-3xl flex gap-2 items-center">
          <QuivrLogo size={64} />
          <div className="cursor-default">Quivr</div>
        </div>
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
              width: "250px",
              backgroundColor: "white",
              borderRadius: "0.75rem",
              paddingTop: "0.5rem",
              paddingInline: "1rem",
              paddingBottom: "1.5rem",
              display: "flex",
              flexDirection: "column",
              gap: "1rem",
              marginRight: "1rem",
              marginTop: "-1rem",
            }}
          >
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
          </Popover.Content>
        </Popover.Root>
      </header>
    </>
  );
};
