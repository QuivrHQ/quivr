import Link from "next/link";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { cn } from "@/lib/utils";

import { PopoverMenuMobile } from "./components/PopoverMenuMobile";
import { useHomeHeader } from "./hooks/useHomeHeader";
import { linkStyle } from "./styles";

type HomeNavProps = {
  color?: "white" | "black";
};

export const HomeHeader = ({ color = "white" }: HomeNavProps): JSX.Element => {
  const { navLinks } = useHomeHeader({ color });

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
