import * as Popover from "@radix-ui/react-popover";
import Image from "next/image";
import Link from "next/link";
import { LuMenu, LuX } from "react-icons/lu";

export const HomeHeader = (): JSX.Element => {
  const navItems = [
    { href: "https://github.com/StanGirard/quivr", label: "Star us on GitHub" },
    { href: "/login", label: "Sign in" },
    { href: "/signup", label: "Sign up" },
  ];

  const navLinks = navItems.map(({ href, label }) => (
    <li key={label}>
      <Link href={href} className="">
        {label}
      </Link>
    </li>
  ));

  return (
    <>
      <header className="w-screen flex justify-between items-center p-5">
        <div className="text-white text-3xl flex gap-2 items-center">
          <Image
            width={64}
            height={64}
            src="/logo-transparent-bg.png"
            alt="logo"
          />
          <div className="cursor-default">Quivr</div>
        </div>
        <Popover.Root>
          <Popover.Trigger>
            <button
              title="menu"
              type="button"
              className="text-white bg-[#D9D9D9] bg-opacity-30 rounded-full px-4 py-1"
            >
              <LuMenu size={32} />
            </button>
          </Popover.Trigger>
          <Popover.Content
            style={{
              width: "max-content",
              backgroundColor: "white",
              borderRadius: "1rem",
              padding: "1rem",
            }}
          >
            <Popover.Close>
              <button title="close" type="button">
                <LuX width="16" height="16" />
              </button>
            </Popover.Close>
            <nav>
              <ul className="flex flex-col">{navLinks}</ul>
            </nav>
          </Popover.Content>
        </Popover.Root>
      </header>
    </>
  );
};
